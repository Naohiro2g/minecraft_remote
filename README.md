# Naohiro2g/minecraft_remote

## BREAKING UPDATE: You can now remotely control the latest version of Minecraft with a plugin instead of mods.
See (https://github.com/Naohiro2g/minecraft_remote_itkids/tree/main/itkids_9) for more info.  I will add a note to that repo and then upgrade this minecraft_remote to the next version.

[**(==== 日本語はこちら。 ====)**](./README_ja.md)

|[1.12 World of Color Update](https://www.youtube.com/watch?v=k2dQuIIUT-o)|[1.13 Update Aquatic](https://www.youtube.com/watch?v=hcutClmY1pI)|[1.16 Nether update](https://www.youtube.com/watch?v=1DhWXAiNgfQ)|
|--|--|--|
|[<img src="./images/1.12_world_of_color_update.jpg" width="240">](./images/1.12_world_of_color_update.jpg)|[<img src="./images/1.13_update_aquatic.jpg" width="240">](./images/1.13_update_aquatic.jpg)|[<img src="./images/1.16_nether_update.png" width="240">](./images/1.16_nether_update.png)|

We had been stucked in the world of color for four years.  The wait is over. You can control over Minecraft Java Edition Version 1.16.5 in Scratch 3 or Python.

## Remote control over Minecraft in Python / Scratch

By using the Minecraft API and coding in Scratch or Python, you can place blocks and move Steve around, and more.

As you know, it is of course fun to do such things manually in the Minecraft world, but it is also fun to code and automatically remote control. And it's an excellent subject to get you interested in learning Scratch or Python.

In my class, we even include the use of git and GitHub.com, which is a fun self-study material for both young learners and experienced ones. **It's a great way to learn a programming language by having something you want to do first.**

I believe the same is true for learning a foreign language. **Don't learn the language, use the language.** (I've just created the 'quote' now. ;) )

## Editions / versions and environments
There are three different environments depending on the combination of Minecraft editions and versions.

Regarding Python modules, the Java version 1.12.2 uses the traditional mcpi as in the Raspi version, while the Java version 1.16.5 uses the new mcje.  The Java version 1.16.5 uses the new mcje. The RasPi version does not require any mods, while each of the two Java versions requires the same version of mods as Minecradt, and a Forge to house the mods.
|Minecraft|Forge|mod|Python module|Scratch + Extension|
|---|---|---|---|---|
|Pi Edition (MCPI) Raspbery Pi|-|-|[mcpi](https://github.com/martinohanlon/mcpi)|Scratch 1.4 + [Scratch2MCPI](https://github.com/scratch2mcpi/scratch2mcpi)|
|Java Edition (MCJE) 1.12.2|[Forge 1.12.2](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.12.2.html)|[RemoteControllerMod-1.12.2 v0.02](https://www.curseforge.com/minecraft/mc-mods/remote-controller/files/3242375)|[mcpi](https://github.com/martinohanlon/mcpi)|[Scratch 3 + MC Ext 1.12.2](https://takecx.github.io/scratch-gui/1-12-2/)|
|Java Edition (MCJE) 1.16.5|[Forge 1.16.5](https://files.minecraftforge.net/net/minecraftforge/forge/index_1.16.5.html)|[RemoteControllerMod-1.16.5 v0.05](https://www.curseforge.com/minecraft/mc-mods/remote-controller/files/3363255)|[mcje](./mcje)|[Scratch 3 + MC Ext 1.16.5](https://takecx.github.io/scratch-gui/1-16-5/)|

***Optifine mod might fine tune on the visual effects of Minecraft Java Edition to make it snappier.You need to select the same version as Minecraft. https://optifine.net/downloads
You might need Java SE 8 JRE to run Forge. https://www.java.com/download/***

You can run Minecraft Java Edition on Linux including Raspberry Pi, Mac and PC. Unfortunately, at least so far, new comer who cannnot have Mojang account are very difficult to launch the Java Edition app on Raspberry Pi. (Minecraft account system is in the middle of migrating from Mojang account to Microsoft one. Arm platform is not on the support list of Microsoft.)

The changes of Minecraft Java Edition at 1.13 "Update Aquatic" were so significant that we were forced to stay with 1.12.2 for three long years in remote control over Minecraft. We broke thruough it by the huge effort of [takecx](https://github.com/takecx), then made it possible to work with version 1.16.5.

But, once again, the changes at version 1.17 was pretty large. For the compatibility with the latest version of Minecraft-Forge 1.17, please wait for a while to cope with it. Or, rather concider to join force with us for the development of [RemoteControllerMod](https://github.com/takecx/RemoteControllerMod) on GitHub.com to reduce the wait.

(The black horse is thinking... to help us?)
[<img src="./images/minecraft_remote_digitalclock.png" width="400">](./images/minecraft_remote_digitalclock.png)

## Examples to draw something in the Minecraft world by voxels or volume pixels
Sorry, examples are only in Python, not for Scratch, so far. See [takecy's](https://github.com/takecx/RemoteControllerMod) to start in Scratch.
 - [hello_MCPI.py](./hello_MCPI.py), [hello_MCJE.py](./hello_MCJE.py), [hello_MCJE1122.py](./hello_MCJE1122.py) : Typical Hello World code. **Try this first to learn how to select Python module mcpi or mcje for your environment.** Install mcpi from Pypi with this. ``` pip3 install mcpi --user ``` or ``` pip install mcpi --user ```

 - [digitalclock.py](digitalclock.py) to display a realtime clock with time and date using 5 x 7, LCD font in the format as follows (also shown in the picture above):
```
        2021-06-26
         21:28:45
```
Using hand-made LCD font on double-buffer display, you can learn 'class'.  I prefer SEA_LANTERN_BLOCK for the time display but unfortunately it's not available in MCPI.

 - [axis_flat.py](axis_flat.py) : Module to draw x, y, and z-axis and to flatten the world in addition. Nice and useful utilities to prepare the world for learning.
  Axes with the virtual origin at (0, 80, 0) for MCJE, or (0, 20, 0) for MCPI using block types as follows:
    - x-axis: Stone blocks
    - y-axis: Grass on soil blocks
    - z-axis: Gold blocks

 - [demo1.py](./demo1.py), [demo2.py](./demo2.py) : Usage of axis_flat or double_buffer_display modules.
 - **(NEW)** [maze.py](./maze.py) : Building a maze in the Minecraft world by supu, Python VTuber. Watch her movie on YouTube : https://www.youtube.com/watch?v=iK3V8q2EiI8
**"Remote Minecraft by Python"** — Let's create a maze automatically and play with it on Minecraft. — In Japanese without English CC, sorry.
   - Using a Python module named mazelib. It contains C++ code and there is no binary on Pypi, it needs to be built during installation with pip.
   - Mac, Linux：
       - You should be successfully install it with ```sudo pip3 install mazelib ```
   - Windows 10／11：
      - If you have C++ build tools, this will help you: ```pip install mazelib``` Or read the details below.

**You might think learning axes or axis are too difficult and too early for age 8, but it's not true. If you are thinking to *teach* them, it's true. Just try to assist kids learning. Umm, I'm just playing with them, actually.**

[<img src="./images/maze_letters.png" width="220">](./images/maze_letters.png) [<img src="./images/maze_blocks.png" width="220">](./images/maze_blocks.png)

(Maze by letters, and by blocks in the Minecraft world.)

### Widows C++ build tools (for mazelib)
https://visualstudio.microsoft.com/downloads/

Open the "Tools for Visual Studio 2022" in the page, then get the "Build Tools for Visual Studio 2022". The app/tool is stand-alone so **you don't need the Visual Studio 2022 itself.**

Launch the app and you will know the name is Visual Studio Installer.
Click the "Modify" then, find and install two components below in the "Individual components" tab.
 1.  Windows 10 SDK or Windows 11 SDK
 1.  MSVC v143 VS2022 C++ x64/x86 build tool (latest)

Search windows sdk for (1), search msvc for (2).

## Files used in the digital clock
#### [digitalclock.py](./digitalclock.py)
 - Main file to run by ```python digitalclock.py```
 - Using two display instances, for date and time, respectively.
 - You need to select a python module from mcpi or mcje to use.
#### [double_buffer_display.py](./double_buffer_display.py)
 - Class BufferDisplay
 - Display class with two flipping buffers to draw only changes from the last time.
 - You need to select a python module from mcpi or mcje to use.
#### [font_5x7.py](./font_5x7.py)
 - 5 x 7 LCD font design
#### [param_MCJE.py](./param_MCJE.py), [param_MCJE1122.py](./param_MCJE1122.py), [param_MCPI.py](./param_MCPI.py)
 - Constant values of several block types, world size, and axis parameters
 - param_MCJE: for Minecraft Java Edition 1.16.5
 - param_MCJE1122: for Minecraft Java Edition 1.12.2
 - param_MCPI: for Minecraft Pi Edition
#### [mcje (minecraft java edition)](./mcje)
 - Python module forked from https://github.com/lasteamlab/mcpi2
 - Named as mcje, and updated for use of Minecraft Java Edition 1.13 or later.
 - It might be available in Pypi later.

## Preparation for Python, Java and other environment

(in the pipeline...)
 - Python 3.7.9
 - Java SE 8 JRE
