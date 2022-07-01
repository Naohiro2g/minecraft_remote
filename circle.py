from mcje.minecraft import Minecraft
import param_MCJE as param
import numpy as np

def setCircle(mc,ca,cb,cc,radius):
    i=0
    rad=np.linspace(0,2*np.pi,1000)
    while i < 1000:
        cx=radius*np.cos(rad[i])
        cz=radius*np.sin(rad[i])
        cx=int(cx)
        cz=int(cz)
        mc.setBlock(cx+ca,cc,cz+cb,param.RED_GLASS)
        i += 1
        
if __name__ == '__main__':
    mc = Minecraft.create(port=param.PORT_MC)
    setCircle(mc,0,0,0,8)
