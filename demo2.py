"""
display digits in the Minecraft world like 1-23:45

AP1 = (-19, 100, -5)  # display frame position
num_of_letters = 7     # display frame width
msg = '1-23:45'       # message to display

You can use numbers, "-", ":", and " ". Or, make your own letters.
"""
# Select modules to import here.
# Minecraft Java Edition 1.16.5 : mcje, param_MCJE
# Minecraft Java Edition 1.12.2 : mcpi, param_MCJE1122
# Minecraft Pi Edition : mcpi, param_MCPI

# for Minecraft Java Edition 1.16.5
from mcje.minecraft import Minecraft
import param_MCJE as param
AP1 = (-19, 100, -5)  # top-left of the display frame

# for Mineraft Java Edition 1.12.2
# from mcje.minecraft import Minecraft
# import param_MCJE1122 as param
# AP1 = (-19, 100, -5)  # top-left of the display frame

# for Mineraft Pi Edition
# from mcpi.minecraft import Minecraft
# import param_MCPI as param
# AP1 = (-19, 63, -5)  # top-left of the display frame


from double_buffer_display import BufferDisplay
import time

# mc = Minecraft.create(address='nao2g005.local', port=param.PORT_MC)
mc = Minecraft.create(port=param.PORT_MC)  # MCJE:14712, MCPI:4711
mc.postToChat("demo2")

num_of_letters = 7
display1 = BufferDisplay(
                mc, anchor_position=AP1,
                num_of_letters=num_of_letters,
                block_frame=param.GOLD_BLOCK)
msg = '1-23:45'
display1.update(msg, block_letters=param.IRON_BLOCK)
mc.postToChat(msg)

time.sleep(4)
msg = '6543210'
display1.update(msg, block_letters=param.GOLD_BLOCK)
mc.postToChat(msg)

time.sleep(4)
display1.delete()
