# Digital date-clock display in the Minecraft world
# YYYY-MM-DD
# HH:MM:SS
# Naohiro Tsuji 2021-06-28

# Select modules to import here.
# Minecraft Java Edition 1.16.5 : mcje, param_MCJE
# Minecraft Java Edition 1.12.2 : mcpi, param_MCJE1122
# Minecraft Pi Edition : mcpi, param_MCPI

from mcje.minecraft import Minecraft
import param_MCJE as param

# from mcpi.minecraft import Minecraft
# import param_MCJE1122 as param

# from mcpi.minecraft import Minecraft
# import param_MCPI as param


import datetime
import time

from double_buffer_display import BufferDisplay


# If you would like to contorl Minecraft running on the other computer:
# mc = Minecraft.create(address='nao2g005.local', port=param.PORT_MC)
# In the case of Minecraft is hosted on this, your computer:
mc = Minecraft.create(port=param.PORT_MC)

# display1 for year, month, and date in YYYY-MM-DD
num_of_letters = len(datetime.datetime.now().strftime("%Y-%m-%d"))
# top-left of the clock frame
ap1 = (0, param.AXIS_Y_V_ORG + 24, 5)
display1 = BufferDisplay(mc, anchor_position=ap1,
                         block_frame=param.GOLD_BLOCK, num_of_letters=num_of_letters)

# display2 for hour, minute, second in HH:MM:SS
num_of_letters = len(time.strftime("%H:%M:%S"))
ap2 = (6, param.AXIS_Y_V_ORG + 12, 5)
display2 = BufferDisplay(mc, anchor_position=ap2,
                         block_frame=param.IRON_BLOCK, num_of_letters=num_of_letters)

msg = datetime.datetime.now().strftime("%Y-%m-%d")
display1.update(msg, block_letters=param.IRON_BLOCK)

while True:
    msg = time.strftime("%H:%M:%S")
    display2.update(msg, block_letters=param.SEA_LANTERN_BLOCK)
    # display2.update(msg, block_letters=param.GLOWSTONE)
    time.sleep(0.1)  # Rest for a while before drawing again.
