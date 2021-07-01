# Digital date-clock display in the Minecraft world
# YYYY-MM-DD
# HH:MM:SS
# Naohiro Tsuji 2021-06-28

import datetime
import time

from double_buffer_display import BufferDisplay

# Minecraft Java Edition 1.13 or later
from mcpi2.minecraft import Minecraft
import param_MCJAVA as param

# Mineraft Pi Edition
# from mcpi.minecraft import Minecraft
# import param_MCPI as param

# mc = Minecraft.create(address='nao2g007', port=param.PORT_MC)
mc = Minecraft.create(port=param.PORT_MC)


# display1 for year, month, and date in YYYY-MM-DD
num_of_digits = len(datetime.datetime.now().strftime("%Y-%m-%d"))
# left-bottom of the clock frame
ap1 = (0, 63, -5)
display1 = BufferDisplay(anchor_position=ap1)
display1.clear(mc, num_of_digits=num_of_digits, block_frame=param.GOLD_BLOCK)

# display2 for hour, minute, second in HH:MM:SS
num_of_digits = len(time.strftime("%H:%M:%S"))
ap2 = (6, 51, -5)
display2 = BufferDisplay(anchor_position=ap2)
display2.clear(mc, num_of_digits=num_of_digits, block_frame=param.IRON_BLOCK)

msg = datetime.datetime.now().strftime("%Y-%m-%d")
display1.render(msg, blockId=param.IRON_BLOCK)
display1.flip(mc)

while True:
    msg = time.strftime("%H:%M:%S")
    display2.render(msg, blockId=param.GLOWSTONE)
    display2.flip(mc)
    time.sleep(0.1)  # Rest for a while before drawing again.
