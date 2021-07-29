# Hello World for Minecraft Pi Edition or Java Edition 1.12.2
# mcpi, MCPI: Minecraft Pi
from mcpi.minecraft import Minecraft
import param_MCPI as param

mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat('Hello Minecraft Pi Edition or Java Edition 1.12.2')
mc.setBlocks(5,0,5, 5,63,5, param.GOLD_BLOCK)
