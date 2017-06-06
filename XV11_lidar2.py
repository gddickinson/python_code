#Display Data from Neato LIDAR
#requires vpython and pyserial

import thread, time, sys, traceback, math
from PIL import ImageGrab

com_port = "COM5" # example: 5 == "COM6" == "/dev/tty5"
baudrate = 115200
visualization = True
offset = 140
init_level = 0
index = 0
imgindex = 1
lidarData = [[] for i in range(360)] #A list of 360 elements Angle, Distance , quality

if visualization:
    from visual import *
    point = points(pos=[(0,0,0) for i in range(360)], size=3, color=(1, 1, 1))
    label_speed = label(pos = (0,-500,0), xoffset=1, box=False, opacity=0.1, visible=False)
    label_errors = label(pos = (0,-1000,0), xoffset=1, text="errors: 0", visible = False, box=False)

def update_view( angle, data ):
    """Updates the view of a sample.
    Takes the angle (an int, from 0 to 359) and the list of four bytes of data in the order they arrived."""

    global offset, use_outer_line, use_line
    x = data[0]
    x1= data[1]
    x2= data[2]
    x3= data[3]

    #angle = (angle + 0) % 360 #adjust for lidar error
    angle_rad = angle * math.pi / 180.0
    c = math.cos(angle_rad)
    s = -math.sin(angle_rad)

    dist_mm = x | (( x1 & 0x3f) << 8) # distance is coded on 13 bits ? 14 bits ?
    quality = x2 | (x3 << 8) # quality is on 16 bits
#    lidarData[angle] = [dist_mm,quality]
    lidarData[359-angle] = [dist_mm,quality] #reversed for Breezy
    dist_mm = dist_mm * .002 #to fit in window
    dist_x = dist_mm*c
    dist_y = dist_mm*s
    if visualization:
        point.pos[angle] = vector( 0, 0, 0 ) #reset the point display
        if not (x1 & 0x80): # is the flag for "bad data" set?
            point.pos[angle] = vector( dist_x, -dist_y, 0)

def checksum(data):
    """Compute and return the checksum as an int.
    data -- list of 20 bytes (as ints), in the order they arrived in."""
    # group the data by word, little-endian
    data_list = []
    for t in range(10):
        data_list.append( data[2*t] + (data[2*t+1]<<8) )

    # compute the checksum on 32 bits
    chk32 = 0
    for d in data_list:
        chk32 = (chk32 << 1) + d

    # return a value wrapped around on 15bits, and truncated to still fit into 15 bits
    checksum = (chk32 & 0x7FFF) + ( chk32 >> 15 ) # wrap around to fit into 15 bits
    checksum = checksum & 0x7FFF # truncate to 15 bits
    return int( checksum )


def gui_update_speed(speed_rpm):
    label_speed.text = "RPM : " + str(speed_rpm)

def compute_speed(data):
    speed_rpm = float( data[0] | (data[1] << 8) ) / 64.0
    return speed_rpm

def read_Lidar():
    global init_level, angle, index

    nb_errors = 0
    while True:
        try:
            time.sleep(0.00001) # do not hog the processor power

            if init_level == 0 :
                b = ord(ser.read(1))
                # start byte
                if b == 0xFA :
                    init_level = 1
                    #print lidarData
                else:
                    init_level = 0
            elif init_level == 1:
                # position index
                b = ord(ser.read(1))
                if b >= 0xA0 and b <= 0xF9 :
                    index = b - 0xA0
                    init_level = 2
                elif b != 0xFA:
                    init_level = 0
            elif init_level == 2 :
                # speed
                b_speed = [ ord(b) for b in ser.read(2)]

                # data
                b_data0 = [ ord(b) for b in ser.read(4)]
                b_data1 = [ ord(b) for b in ser.read(4)]
                b_data2 = [ ord(b) for b in ser.read(4)]
                b_data3 = [ ord(b) for b in ser.read(4)]

                # for the checksum, we need all the data of the packet...
                # this could be collected in a more elegent fashion...
                all_data = [ 0xFA, index+0xA0 ] + b_speed + b_data0 + b_data1 + b_data2 + b_data3

                # checksum
                b_checksum = [ ord(b) for b in ser.read(2) ]
                incoming_checksum = int(b_checksum[0]) + (int(b_checksum[1]) << 8)

                # verify that the received checksum is equal to the one computed from the data
                if checksum(all_data) == incoming_checksum:
                    speed_rpm = compute_speed(b_speed)
                    if visualization:
                        gui_update_speed(speed_rpm)

                    update_view(index * 4 + 0, b_data0)
                    update_view(index * 4 + 1, b_data1)
                    update_view(index * 4 + 2, b_data2)
                    update_view(index * 4 + 3, b_data3)
                else:
                    # the checksum does not match, something went wrong...
                    nb_errors +=1
                    if visualization:
                        label_errors.text = "errors: "+str(nb_errors)

                    # display the samples in an error state
                    update_view(index * 4 + 0, [0, 0x80, 0, 0])
                    update_view(index * 4 + 1, [0, 0x80, 0, 0])
                    update_view(index * 4 + 2, [0, 0x80, 0, 0])
                    update_view(index * 4 + 3, [0, 0x80, 0, 0])

                init_level = 0 # reset and wait for the next packet

            else: # default, should never happen...
                init_level = 0
        except :
            traceback.print_exc(file=sys.stdout)

def write_data(datadir, datafile, lidarData):
    baseStr = "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0  "
    with open(datadir + "/" + datafile, "a") as lfile:
        dataStr = baseStr
        for ang in lidarData:
            if len(ang)>0:
                dataStr += str(ang[0])
            else:
                dataStr += "0"
            dataStr += " "
        lfile.write("\n" + dataStr)

def checkKeys():
    global imgindex
    if scene.kb.keys: # event waiting to be processed?
        s = scene.kb.getkey() # get keyboard info
        if s=="r": # Toggle rpm
            label_speed.visible = not label_speed.visible
        elif s=="e": # Toggle errors
            label_errors.visible = not label_errors.visible
##        elif s=="s": #saveimage
##            im = ImageGrab.grab((8,30,420,420))
##            im.save('scan-' + str(imgindex) + '.png')
##            print "Image saved"
##            imgindex += 1
        elif s=="x":
            exit()

import serial
ser = serial.Serial(com_port, baudrate)
th = thread.start_new_thread(read_Lidar, ())

while True:
    if visualization:
        rate(60) # synchonous repaint at 60fps
        scene.autoscale = False
        #write_data('../BreezySLAM/examples', 'lidar.dat', lidarData)
        write_data(r'C:/Users/George/Documents/BreezySLAM/examples', 'lidar.dat', lidarData)
        checkKeys()
        time.sleep(.2)
