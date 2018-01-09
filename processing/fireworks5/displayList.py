from fireworks import Firework
from random import randint


def getList(showWanted = "test"):
    
    show1 = ([\
    [Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1, repeat=False),1],\
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 15, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_H", repeat=False),2],\    
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "A", repeat=False),3],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "P", repeat=False),4],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "P", repeat=False),4],\ 
    [Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "Y", repeat=False),4],\                                                
    [Firework(startPosition=-100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "upper_B", repeat=False),20],\ 
    [Firework(startPosition=-75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "I", repeat=False),21],\ 
    [Firework(startPosition=-25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "R", repeat=False),22],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "T", repeat=False),23],\                                                
    [Firework(startPosition=25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "H", repeat=False),24],\ 
    [Firework(startPosition=50,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "D", repeat=False),25],\ 
    [Firework(startPosition=75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "A", repeat=False),26],\ 
    [Firework(startPosition=100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "Y", repeat=False),27],\
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_S", repeat=False),100],\                                                
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "U", repeat=False),120],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "S", repeat=False),140],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "A", repeat=False),160],\ 
    [Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "N", repeat=False),180],\
    [Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+10, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=True, flare = True),200],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+30, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=True, flare = True),200],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+70, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=True, flare = True),250],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+50, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=True, flare = True),250],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+100, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=True, flare = True),250],\
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "cake", repeat=False, flare=True, flareSize =20),500],\
        ]) 

    if showWanted == "show1":
        return show1
    
    test = ([\      
        [Firework(startPosition=0,setDirection=True,numberOfParticules=10, direction=0, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -9, repeat=False, flare=True, flareSize =20),1],\
        ])

    if showWanted == "test":
        return test                              
                                                                                          
    return None