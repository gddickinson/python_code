import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import numpy as np
import alsaaudio, time, audioop
import scipy

def update_line(num, data, line):
    data = soundRecord()
    line.set_data(data[...,:num])
    #print (data)
    return line,

def soundRecord():
    # Open the device in nonblocking capture mode. The last argument could
    # just as well have been zero for blocking mode. Then we could have
    # left out the sleep call in the bottom of the loop
    inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK)
    
    # Set attributes: Mono, 8000 Hz, 16 bit little endian samples
    inp.setchannels(1)
    inp.setrate(8000)
    inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    
    # The period size controls the internal number of frames per period.
    # The significance of this parameter is documented in the ALSA api.
    # For our purposes, it is suficcient to know that reads from the device
    # will return this many frames. Each frame being 2 bytes long.
    # This means that the reads below will return either 320 bytes of data
    # or 0 bytes of data. The latter is possible because we are in nonblocking
    # mode.
    inp.setperiodsize(160)
    x = []
    y = []
    i=0
    while i<4:
        # Read data from device
        l,data = inp.read()
        if l:
        	# Return the maximum of the absolute value of all samples in a fragment.
         #print (l)
         x.append(audioop.rms(data,2))
         y.append(i)
         #print audioop.max(data, 2)
         i+=1
         time.sleep(.001)
    x=np.array((y,x))
    freq = scipy.fft(x[:,1])
    Xdb = 20*scipy.log10(scipy.absolute(freq))
   
    
    print (y,frequencies)
    #print x
    return x

fig1 = plt.figure()


l, = plt.plot([], [], 'r--')
plt.xlim(0, 3)
plt.ylim(0, 2000)
plt.xlabel('x')
plt.title('Power')

data = np.array((0,0))
line_ani = animation.FuncAnimation(fig1, update_line, 25, fargs=(data, l), interval=5, blit=True)
#line_ani.save('lines.mp4')


plt.show()
