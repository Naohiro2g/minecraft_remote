# Naohiro2g/minecraft_remote
## Remote control over Minecraft in Python / Scratch

|Minecraft|Forge|mod|Python module|Scratch / Extension|
|---|---|---|---|---|
|Pi Edition|-|-|[mcpi](https://github.com/martinohanlon/mcpi)|Scratch 1.4 / [Scratch2MCPI](https://github.com/scratch2mcpi/scratch2mcpi)|
|Java Edition 1.12.2|[Forge 1.12.2](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.12.2.html)|[RemoteControllerMod-1.12.2 v0.02](https://www.curseforge.com/minecraft/mc-mods/remote-controller/files/3242375)|[mcpi](https://github.com/martinohanlon/mcpi)|[Scratch 3 / MC Ext 1.12.2](https://takecx.github.io/scratch-gui/1-12-2/)|
|Java Edition 1.16.5|[Forge 1.16.5](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)|[RemoteControllerMod-1.16.5 v0.05](https://www.curseforge.com/minecraft/mc-mods/remote-controller/files/3363255)|mcpi2 (here)|[Scratch 3 / MC Ext 1.16.5](https://takecx.github.io/scratch-gui/1-16-5/)|


[<img src="./minecraft_remote_digitalclock.png" width="400">](./minecraft_remote_digitalclock.png)

## Two examples to draw something in the Minecraft world by voxels or volume pixels
 - digitalclock.py to display clock with date using 5 x 7, LCD font in the format as follows:
```
        2021-06-26
        21:28:45
```
 - axis.py to draw x, y, and z-axis with the virtual origin at (0, 80, 0) using block types as follows:
    - x-axis: Stone blocks
    - y-axis: Grass on soil blocks
    - z-axis: Gold blocks
## Files used in the digital clock
#### [digitalclock.py](./digitalclock.py)
 - Main file to run by ```python digitalclock.py```
 - Using two display instances, for date and time, respectively.
#### [double_buffer_display.py](./double_buffer_display.py)
 - Class BufferDisplay(anchor_position=Vec3(0,80,0))
 - Display class with two flipping buffers to draw only changes from the last time.
#### [font_5x7.py](./font_5x7.py)
 - 5 x 7 LCD font design
#### [param_MCJAVA.py](./param_MCJAVA.py), [param_MCPI.py](./param_MCPI.py)
 - Constant values of several block types, world size, and axis parameters
#### [mcpi2](./mcpi2)
 - forked from https://github.com/lasteamlab/mcpi2
 - mcpi (Minecraft Pi) module, updated for use of Minecraft Java Edition 1.13 or later.
 - In the case of using sample codes for Minecraft Pi edition and Java Edition 12.2 or earlier, just replace the line ```from mcpi2.minecraft import Minecraft``` with ```from mcpi.minecraft import Minecraft```
