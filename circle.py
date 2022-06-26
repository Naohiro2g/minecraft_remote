from mcje.minecraft import Minecraft
import param_MCJE as param
import numpy as np

def setCircle(mc,ca,cb,radius):
    i=0
    rad=np.linspace(0,2*np.pi,100)
    while i < 100:
        cx=radius*np.cos(rad[i])
        cz=radius*np.sin(rad[i])
        cx=int(cx)
        cz=int(cz)
        mc.setBlock(cx+ca,80,cz+cb,param.LIME_CONCRETE)
        i += 1
        
if __name__ == '__main__':
    mc = Minecraft.create(port=param.PORT_MC)
    setCircle(mc,0,0,8)
