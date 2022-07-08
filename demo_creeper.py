from mcje.minecraft import Minecraft
import param_MCJE as param
from time import sleep
from creeper import set_creeper, clear_creeper

mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat("Creepers!")

set_creeper(mc, z=20, y=75)
sleep(1)
clear_creeper(mc, z=20, y=75)
set_creeper(mc, x=20, z=-20, block_id="pink_wool", block_eye_id="green_wool")
sleep(1)
clear_creeper(mc, x=20, z=-20)
