from fireworks import Firework
from random import randint


def getList(showWanted = "test"):
    
    show1 = ([\
    [Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1, repeat=False),1],\
    [Firework(setRocketVelocity = True, rocketVelocity = -7, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1, repeat=False),1],\
    [Firework(setRocketVelocity = True, rocketVelocity = -9, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=0, repeat=False),1],\
    [Firework(startPosition=-100,setDirection=True,numberOfParticules=10, direction=3, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -10, repeat=False, flare=True, flareSize =20),5],\
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 15, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_H", repeat=False),60],\    
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "A", repeat=False),63],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "P", repeat=False),65],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "P", repeat=False),66],\ 
    [Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "Y", repeat=False),67],\                                                
    [Firework(startPosition=-100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "upper_B", repeat=False),70],\ 
    [Firework(startPosition=-75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "I", repeat=False),71],\ 
    [Firework(startPosition=-25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "R", repeat=False),72],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "T", repeat=False),73],\                                                
    [Firework(startPosition=25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "H", repeat=False),74],\ 
    [Firework(startPosition=50,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "D", repeat=False),75],\ 
    [Firework(startPosition=75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "A", repeat=False),76],\ 
    [Firework(startPosition=100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "Y", repeat=False),77],\
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_S", repeat=False),140],\                                                
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "U", repeat=False),160],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "S", repeat=False),170],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "A", repeat=False),180],\ 
    [Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "N", repeat=False),210],\
    [Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+10, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = False),250],\
    [Firework(startPosition=100,setDirection=True,numberOfParticules=20, direction=-2, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -9, repeat=False, flare=True, flareSize =20),250],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+30, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),250],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+70, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),300],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+50, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+100, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+50, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+100, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "cake", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),500],\
        ]) 

    if showWanted == "show1":
        return show1
    
    test = ([\      
        [Firework(startPosition=-100,setDirection=True,numberOfParticules=10, direction=3, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -10, repeat=False, flare=True, flareSize =20),1],\
        ])

    if showWanted == "test":
        return test                              
                                                                                          
    return None