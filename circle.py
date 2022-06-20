from mcje.minecraft import Minecraft
import param_MCJE as param
from time import sleep
import numpy as np

def setCircle(wait=0.1):
    mc = Minecraft.create(port=param.PORT_MC)
    mc.postToChat("succeed?")
    radius=8
    i=0
    rad=np.linspace(0,2*np.pi,100)
    cx=radius*np.cos(rad[i])
    cz=radius*np.sin(rad[i])
    int(cx,cz)
    while i < 100:
        i += 1
        mc.setBlock(cx,70,cz,param.DIAMOND_BLOCK)
        sleep(wait)
        mc.postToChat(i)
        
setCircle()
