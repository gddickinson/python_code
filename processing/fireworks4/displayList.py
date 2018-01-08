from fireworks import Firework

def getList():

    showList = ([[Firework(setRocketVelocity = True, rocketVelocity = -10, setExplosionSize = True, explosionSize=50, explosionDuration = 5, setDirection=True, direction=1, repeat=False),1],\
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
    ]) 
    
    return showList