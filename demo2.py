"""
display digits in the Minecraft world like 1-23:45

AP1 = (-19, 100, -5)  # display frame position
num_of_digits = 7     # display frame width
msg = '1-23:45'       # message to display

You can use numbers, "-", ":", and " ". Or, make your own letters.
"""

# for Minecraft Java Edition 1.16.5
from mcje.minecraft import Minecraft
import param_MCJE as param
AP1 = (-19, 100, -5)  # top-left of the display frame

# for Mineraft Pi Edition or Java Edition 1.12.2
# from mcpi.minecraft import Minecraft
# import param_MCPI as param
# AP1 = (-19, 63, -5)  # top-left of the display frame

from double_buffer_display import BufferDisplay

# mc = Minecraft.create(address='nao2g007.local', port=param.PORT_MC)
mc = Minecraft.create(port=param.PORT_MC)  # MCJE:14712, MCPI:4711
mc.postToChat("demo2")

num_of_digits = 7
display1 = BufferDisplay(anchor_position=AP1)
display1.clear(mc, num_of_digits=num_of_digits, block_frame=param.GOLD_BLOCK)

msg = '1-23:45'
display1.render(msg, blockId=param.IRON_BLOCK)
display1.flip(mc)
