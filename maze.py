# Maze builder in Minecraft world
#
# Original code written by PythonVTuberサプー or supu
# https://colab.research.google.com/drive/1asGAz0ggpt4d-cVYPhyWkk_lTqTRNF-A
# Copyright (c) 2021 supu  Released under the MIT license
# YouTube:【Pythonでマイクラ操作！】自動で迷路を作成してマインクラフト上で遊んでみよう
#       〜 Minecraftプログラミング入門 〜    https://www.youtube.com/watch?v=iK3V8q2EiI8

from time import sleep
from mazelib import Maze
from mazelib.generate.Prims import Prims
# from mcpi import minecraft, block

# Select modules to import here.
# Minecraft Java Edition 1.16.5 : mcje, param_MCJE
# Minecraft Java Edition 1.12.2 : mcpi, param_MCJE1122
# Minecraft Pi Edition : mcpi, param_MCPI

# from mcje.minecraft import Minecraft
# import param_MCJE as param

from mcpi.minecraft import Minecraft
import param_MCJE1122 as param

# from mcpi.minecraft import Minecraft
# import param_MCPI as param

N = 5
M = 8
H = 3


def put_maze_block(mc, mark, x_pos, z_pos):
    if mark == '#':
        mc.setBlocks(
            x_pos, param.Y_SEA + 1, z_pos,
            x_pos, param.Y_SEA + 1 + H, z_pos,
            param.SEA_LANTERN_BLOCK
        )


def main(wait=0.1):
    mc = Minecraft.create()
    mc.player.setPos(12, 80, 12)

    mc.setBlocks(
        -40, param.Y_SEA + 1, -40,
        40, 127, 40,
        param.AIR
    )

    mc.setBlocks(
        -40, param.Y_SEA - 1, -40,
        40, param.Y_SEA - 1, 40,
        param.STONE
    )

    mc.setBlocks(
        -40, param.Y_SEA, -40,
        40, param.Y_SEA, 40,
        param.GRASS_BLOCK
    )

    mz = Maze()
    mz.generator = Prims(N, M)

    mz.generate()
    mz.start = (0, 1)
    mz.end = (N * 2, M * 2 - 1)
    maze_str = str(mz)
    maze_list = maze_str.split('\n')

    for z, mark_list in enumerate(maze_list):
        for x, mark in enumerate(mark_list):
            put_maze_block(mc, mark, x, z)
            print(mark + mark, flush=False, end=' ')
            sleep(wait)
        print()


if __name__ == '__main__':
    main(wait=0.05)
