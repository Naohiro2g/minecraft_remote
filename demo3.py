"""
Flatten the world and draw xyz axis.
x: stone, y: grass/dirt, z: gold
The dotted part of the axis means negative region.
The intersection is not the real origin, but a virtual one.
"""
# Select modules to import here.
# Minecraft Java Edition 1.16.5 : mcje, param_MCJE
# Minecraft Java Edition 1.12.2 : mcpi, param_MCJE1122
# Minecraft Pi Edition : mcpi, param_MCPI

# for Minecraft Java Edition 1.16.5
from mcje.minecraft import Minecraft
import param_MCJE as param

# for Mineraft Java Edition 1.12.2
# from mcje.minecraft import Minecraft
# import param_MCJE1122 as param

# for Mineraft Pi Edition
# from mcpi.minecraft import Minecraft
# import param_MCPI as param

import axis_flat


# mc = Minecraft.create(address='nao2g005', port=param.PORT_MC)

mc = Minecraft.create(port=param.PORT_MC)  # MCJE:14712, MCPI:4711

mc.postToChat("demo3")

# In Java Edition, you can use Japanese or other laguages.
mc.postToChat("こんにちは！")


# for MCJE 1.12.2
# mc.player.setPos(0,100,0)
# mc.setBlocks(-80, 60, -80,   80, 120, 80,   0)


axis_flat.reset_minecraft_world(mc, width=40)

mc.postToChat("クリーパーの頭を作る")
x=5
y=63
z=10
BLOCK1=param.GOLD_BLOCK
BLOCK2=param.BLACK_WOOL_BLOCK
mc.setBlocks(x, y, z, x-7, y+7, z+7, BLOCK1)

mc.setBlocks(x-2, y, z, x-2, y+2, z, BLOCK2)

mc.setBlocks(x-5, y, z, x-5, y+2, z, BLOCK2)

mc.setBlocks(x-3, y+1, z, x-4, y+3, z, BLOCK2)

mc.setBlocks(x-1, y+4, z, x-2, y+5, z, BLOCK2)

mc.setBlocks(x-6, y+4, z, x-5, y+5, z, BLOCK2)

mc.postToChat("完成！！！")

