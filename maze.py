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
H = 3
SEA_LEVEL = 62
SEA_LANTERN = 169

def put_maze_block(mc, mark, x_pos, z_pos):
    if mark == '#':
        mc.setBlocks(
            x_pos, SEA_LEVEL + 1, z_pos,
            x_pos, SEA_LEVEL + 1 + H, z_pos,
            SEA_LANTERN  # SEA_LANTERN block not available in mcpi
        )


def main():
    mc = minecraft.Minecraft.create()
    mc.player.setPos(0, 80, 0)

    mc.setBlocks(
        -40, SEA_LEVEL + 1, -40,
        40, 127, 40,
        block.AIR
    )

    mc.setBlocks(
        -40, SEA_LEVEL - 1, -40,
        40, SEA_LEVEL - 1, 40,
        block.STONE
    )

    mc.setBlocks(
        -40, SEA_LEVEL, -40,
        40, SEA_LEVEL, 40,
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
