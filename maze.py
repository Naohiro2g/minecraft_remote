# Maze builder in Minecraft world
#
# Written by PythonVTuberサプー
# 動画：【Pythonでマイクラ操作！】自動で迷路を作成してマインクラフト上で遊んでみよう
#       〜 Minecraftプログラミング入門 〜    https://www.youtube.com/watch?v=iK3V8q2EiI8
# Original code : https://colab.research.google.com/drive/1asGAz0ggpt4d-cVYPhyWkk_lTqTRNF-A

from mazelib import Maze
from mazelib.generate.Prims import Prims
from mcpi import minecraft, block

N = 5
M = 5
H = 2


def put_maze_block(mc, mark, x_pos, z_pos):
    if mark == '#':
        mc.setBlocks(
            x_pos, 0, z_pos,
            x_pos, H, z_pos,
            169  # SEA_LANTERN block not avaiable in mcpi
        )


def main():
    mc = minecraft.Minecraft.create()
    mc.player.setPos(0, 1, 0)

    mc.setBlocks(
        -3, 0, -3,
        50, 50, 50,
        block.AIR
    )

    mc.setBlocks(
        -3, 0, -3,
        50, 0, 50,
        block.GRASS
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
            print(mark)


if __name__ == '__main__':
    main()
