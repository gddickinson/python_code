#mac
pathName = '/Users/george/Desktop/text/'

#pc
pathName = 'C:\\Google Drive\\text\\'

def getRandomPointInLetter(x, y, n, scaleFactor,character = "upper_A"):
    ans = []
    path = pathName + character + '.png'
    img = loadImage(path)
    for i in range(n*10):
        imgX = int(random(img.width))
        imgY = int(random(img.height))
        pix = img.get(imgX,imgY)
        if pix == -1:
            ans.append([((imgX/scaleFactor)-((img.width/2)/scaleFactor))+x,((imgY/scaleFactor)-((img.height/8)/scaleFactor))+y])
    return ans
        
def getRandomPointInJPG(x, y, n, scaleFactor,imgName = "tree"):
    ans = []
    path = pathName + imgName+ '.jpeg'
    img = loadImage(path)
    for i in range(n*10):
        imgX = int(random(img.width))
        imgY = int(random(img.height))
        pix = img.get(imgX,imgY)
        if pix != -1:
            ans.append([((imgX/scaleFactor)-((img.width/2)/scaleFactor))+x,((imgY/scaleFactor)-((img.height/8)/scaleFactor))+y])
    return ans