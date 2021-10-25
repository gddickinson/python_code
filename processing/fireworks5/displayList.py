from fireworks import Firework
from random import randint


def getList(showWanted = "test"):
    
    show1 = ([\
    [Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1, repeat=False),1],\
    [Firework(setRocketVelocity = True, rocketVelocity = -7, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1, repeat=False),1],\
    [Firework(setRocketVelocity = True, rocketVelocity = -9, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=0, repeat=False),1],\
    [Firework(startPosition=-100,setDirection=True,numberOfParticules=10, direction=3, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -10, repeat=False, flare=True, flareSize =20),5],\
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 15, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_H", repeat=False),56],\    
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "A", repeat=False),63],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "P", repeat=False),65],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "P", repeat=False),66],\ 
    [Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "Y", repeat=False),67],\                                                
    [Firework(startPosition=-100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "upper_B", repeat=False),70],\ 
    [Firework(startPosition=-75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "I", repeat=False),73],\ 
    [Firework(startPosition=-25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "R", repeat=False),75],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "T", repeat=False),78],\                                                
    [Firework(startPosition=25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "H", repeat=False),83],\ 
    [Firework(startPosition=50,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "D", repeat=False),87],\ 
    [Firework(startPosition=75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "A", repeat=False),91],\ 
    [Firework(startPosition=100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "Y", repeat=False),96],\
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 30, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_M", repeat=False),140],\                                                
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "A", repeat=False),160],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "R", repeat=False),170],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "Y", repeat=False),180],\ 
    [Firework(startPosition=-90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 15, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_S", repeat=False),190],\    
    [Firework(startPosition=-45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "W", repeat=False),200],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -9, character = "E", repeat=False),210],\ 
    [Firework(startPosition=45,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "R", repeat=False),220],\ 
    [Firework(startPosition=90,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "T", repeat=False),230],\                                                
    [Firework(startPosition=-100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "upper_L", repeat=False),240],\ 
    [Firework(startPosition=-75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "O", repeat=False),240],\ 
    [Firework(startPosition=-25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "V", repeat=False),240],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -7, character = "E", repeat=False),240],\                                                
    [Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+10, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = False),250],\
    [Firework(startPosition=100,setDirection=True,numberOfParticules=20, direction=-2, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -9, repeat=False, flare=True, flareSize =20),250],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+30, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),250],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+70, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),300],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+50, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+100, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+50, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-90,setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=randint(0,20)+100, explosionDuration = 10, setDirection=True, direction=randint(0,2), repeat=False, flare = True),320],\
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_4", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),370],\
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=2, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_6", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),400],\    
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=-1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_1", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),450],\     
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=-1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_4", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),500],\       
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_4", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),550],\       
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_6", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),600],\       
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=-1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_1", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),650],\       
    [Firework(startPosition=-50,setDirection=True,numberOfParticules=10, direction=1, explosionsOn=False, explosionDuration = 20, characterRocket = False, imageRocket = True, setRocketVelocity = True, rocketVelocity = -9, imageName = "dog_5", repeat=False, flare=True, flareSize =20, explosionTypeFlag=False,),700],\  
        [Firework(startPosition=-100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "upper_L", repeat=False),715],\ 
    [Firework(startPosition=-75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "O", repeat=False),715],\ 
    [Firework(startPosition=-25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "V", repeat=False),715],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 20, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "E", repeat=False),715],\  
        [Firework(startPosition=-100,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "upper_Y", repeat=False),730],\ 
    [Firework(startPosition=-75,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "O", repeat=False),730],\ 
    [Firework(startPosition=-25,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 10, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "U", repeat=False),730],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 50, characterRocket = True, setRocketVelocity = True, rocketVelocity = -11, character = "X", repeat=False),750],\   
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 50, characterRocket = True, setRocketVelocity = True, rocketVelocity = -10, character = "X", repeat=False),755],\ 
    [Firework(startPosition=0,setDirection=True, direction=0, explosionsOn=False, explosionDuration = 50, characterRocket = True, setRocketVelocity = True, rocketVelocity = -8, character = "X", repeat=False),760],\     
           ]) 

    if showWanted == "show1":
        return show1
    
    test = ([\      
        [Firework(startPosition=-100,setDirection=True,numberOfParticules=10, direction=3, explosionsOn=False, explosionDuration = 40, explosionTypeFlag=True, setRocketVelocity = True, rocketVelocity = -10, repeat=False, flare=True, flareSize =20),1],\
        ])

    if showWanted == "test":
        return test                              
                                                                                          
    return None