from mcje.minecraft import Minecraft
import param_MCJE as param
import numpy as np

def setCircle(mc,ca,cb,cc,radius,block):
    a = radius*8
    rad=np.linspace(0,2*np.pi,a)
    for i in range(a):
        cx=int(radius*np.cos(rad[i]))
        cz=int(radius*np.sin(rad[i]))
        mc.setBlock(cx+ca,cb,cz+cc,block)

if __name__ == '__main__':
    mc = Minecraft.create(port=param.PORT_MC)
    setCircle(mc,0,60,0,13,param.LIME_CONCRETE)
