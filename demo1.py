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
# from mcje.minecraft import Minecraft
# import param_MCJE as param

# for Mineraft Java Edition 1.12.2
# from mcje.minecraft import Minecraft
# import param_MCJE1122 as param

# for Mineraft Pi Edition
from mcpi.minecraft import Minecraft
import param_MCPI as param

import axis_flat


# mc = Minecraft.create(address='nao2g005', port=param.PORT_MC)

mc = Minecraft.create(port=param.PORT_MC)  # MCJE:14712, MCPI:4711
mc.postToChat("demo1")

# In Java Edition, you can use Japanese or other laguages.
mc.postToChat("こんにちは！")

# for MCJE 1.12.2
# mc.player.setPos(0,100,0)
# mc.setBlocks(-80, 60, -80,   80, 120, 80,   0)


axis_flat.reset_minecraft_world(mc, width=40)
axis_flat.clear_XYZ_axis(mc, wait=0)
axis_flat.draw_XYZ_axis(mc, wait=0.3)
