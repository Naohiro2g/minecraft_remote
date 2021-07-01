from mcpi2.minecraft import Minecraft
import param_MCJAVA as param

# from mcpi.minecraft import Minecraft
# import param_MCPI as param

from time import sleep


# mc = Minecraft.create(address='nao2g007', port=param.PORT_MC)
mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat("axis module loaded")

def draw_XYZ_axis(mc=mc, wait=0.1):

    blockTypeIdX = param.STONE
    blockTypeIdY = param.GRASS_BLOCK
    blockTypeIdZ = param.GOLD_BLOCK
    BLOCK_TOP_LIGHT = param.GLOWSTONE

    # x-axis
    mc.postToChat("x-axis")
    x, y, z = param.AXIS_WIDTH * -1, param.AXIS_Y_V_ORG, 0
    while x <= param.AXIS_WIDTH:
        mc.setBlock(x, y, z, blockTypeIdX)
        if x < 0:
            x += 2
            sleep(wait * 2)
        else:
            x += 1
            sleep(wait)
    # y-axis
    mc.postToChat("y-axis")
    x, y, z = 0, param.AXIS_BOTTOM, 0
    while y <= param.AXIS_TOP - 5:
        mc.setBlock(x, y, z, blockTypeIdY)
        if y < param.AXIS_Y_V_ORG:
            y += 2
            sleep(wait * 2)
        else:
            y += 1
            sleep(wait)
    while y <= param.AXIS_TOP:
        mc.setBlock(x, y, z, BLOCK_TOP_LIGHT)
        y += 1
        sleep(wait)
    # z-axis
    mc.postToChat("z-axis")
    x, y, z = 0, param.AXIS_Y_V_ORG, param.AXIS_WIDTH * -1
    while z <= param.AXIS_WIDTH:
        mc.setBlock(x, y, z, blockTypeIdZ)
        if z < 0:
            z += 2
            sleep(wait * 2)
        else:
            z += 1
            sleep(wait)

def clear_XYZ_axis(mc=mc, wait=0.5):
    mc.setBlocks(param.AXIS_WIDTH * -1, param.AXIS_Y_V_ORG, 0,   param.AXIS_WIDTH, param.AXIS_Y_V_ORG, 0,   param.AIR)  # x
    sleep(wait)
    mc.setBlocks(0, 0, 0,   0, param.AXIS_TOP, 0,   param.AIR)  # y
    sleep(wait)
    mc.setBlocks(0, param.AXIS_Y_V_ORG, param.AXIS_WIDTH * -1,   0, param.AXIS_Y_V_ORG, param.AXIS_WIDTH,   param.AIR)  # z
    sleep(wait)

def reset_Minecraft_World(mc=mc, width=80):
    mc.setBlocks(width * -1, param.AXIS_BOTTOM + 1, width * -1,   width, param.AXIS_TOP,    width,    param.AIR)
    mc.setBlocks(width * -1, param.AXIS_BOTTOM,     width * -1,   width, param.AXIS_BOTTOM, width,    param.GRASS_BLOCK)


if __name__ == "__main__":
    mc.postToChat("main part")

    # if MCJAVA 1.12.2 or earlier
    # mc.player.setPos(0,100,0)
    # mc.setBlocks(-80, 60, -80,   80, 120, 80,   0)

    reset_Minecraft_World()
    # draw_XYZ_axis(wait=0.2)
    # clear_XYZ_axis(wait=0)

    draw_XYZ_axis(wait=0.3)
