# Hello World for Minecraft Pi Edition
# mcpi, MCPI: Minecraft Pi
from mcpi.minecraft import Minecraft
import param_MCPI as param

# mc = Minecraft.create(address='nao2g005', port=param.PORT_MC)
mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat('Hello Minecraft Pi Edition')
mc.setBlocks(-5, 0, 5,  -5, 63, 5,  param.GOLD_BLOCK)
