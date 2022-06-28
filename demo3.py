from mcje.minecraft import Minecraft
import param_MCJE as param

mc = Minecraft.create(port=param.PORT_MC)
mc.setBlock(50,70,50,param.SEA_LANTERN_BLOCK)
mc.setBlocks()