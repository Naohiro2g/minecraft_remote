from mcje.minecraft import Minecraft
import param_MCJE as param
import numpy as np

def setCircle(mc,radius):
    i=0
    rad=np.linspace(0,2*np.pi,5*radius)
    cx=radius*np.cos(rad[i])
    cz=radius*np.sin(rad[i])
    int(cx,cz)
    while i < 100:
        i += 1
        mc.setBlock(cx,70,cz,param.DIAMOND_BLOCK)
        
if __name__ == '__main__'
    mc = Minecraft.create(port=param.PORT_MC)
    setCircle(mc,8)
