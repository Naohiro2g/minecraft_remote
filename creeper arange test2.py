def set_creeper(mc, x=0, z=0, y=63, block_id="gold_block", block_face_id="black_wool", face="1"):
    mc.setBlocks(x, y, z, x-7, y+7, z+7, block_id)
    if face == "1": #normal
        mc.setBlocks(x-2, y, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y+1, z, x-4, y+3, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+5, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "2": #smile
        mc.setBlocks(x-2, y+1, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y+1, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y, z, x-4, y+1, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+5, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "3": #smile_wink
        mc.setBlocks(x-2, y+1, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y+1, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y, z, x-4, y+1, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+4, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "4": #wink
       mc.setBlocks(x-2, y, z, x-2, y+2, z, block_face_id)
       mc.setBlocks(x-5, y, z, x-5, y+2, z, block_face_id)
       mc.setBlocks(x-3, y+1, z, x-4, y+3, z, block_face_id)
       mc.setBlocks(x-1, y+4, z, x-2, y+4, z, block_face_id)
       mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "5": #wow!
        mc.setBlocks(x-2, y, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y, z, x-4, y+3, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+5, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)




def clear_creeper(mc, x=0, z=0, y=63):
    mc.setBlocks(x, y, z, x-7, y+7, z+7, "air_block")


print("creeper module loaded")

if __name__ == "__main__":
    from mcje.minecraft import Minecraft
    import param_MCJE as param
    from time import sleep

    mc = Minecraft.create(port=param.PORT_MC)
    mc.postToChat("Creepers!")

    mc.setBlocks(-40, 63, -40, 40, 85, 40, "air_block")
    sleep(10)
    for x in range(-2, 3):
        set_creeper(mc, x=x * 10, block_id="green_wool", face="2")
        sleep(2)
        # clear_creeper(mc, x=x * 10)

    set_creeper(mc, y=75)
    sleep(1)
    set_creeper(mc, z=-20, block_id="pink_wool", block_face_id="green_wool", face="5")

    mc.postToChat("完成！！！")
