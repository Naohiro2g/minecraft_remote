def set_creeper(mc, x=0, z=0, y=63, block_id="gold_block", block_face_id="black_wool", face="normal"):
    mc.setBlocks(x, y, z, x-7, y+7, z+7, block_id)
    if face == "normal":
        mc.setBlocks(x-2, y, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y+1, z, x-4, y+3, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+5, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "smile":
        mc.setBlocks(x-2, y+1, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y+1, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y, z, x-4, y+1, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+5, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "smile_wink":
        mc.setBlocks(x-2, y+1, z, x-2, y+2, z, block_face_id)
        mc.setBlocks(x-5, y+1, z, x-5, y+2, z, block_face_id)
        mc.setBlocks(x-3, y, z, x-4, y+1, z, block_face_id)
        mc.setBlocks(x-1, y+4, z, x-2, y+4, z, block_face_id)
        mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "wink":
       mc.setBlocks(x-2, y, z, x-2, y+2, z, block_face_id)
       mc.setBlocks(x-5, y, z, x-5, y+2, z, block_face_id)
       mc.setBlocks(x-3, y+1, z, x-4, y+3, z, block_face_id)
       mc.setBlocks(x-1, y+4, z, x-2, y+4, z, block_face_id)
       mc.setBlocks(x-6, y+4, z, x-5, y+5, z, block_face_id)
    elif face == "wow!":
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
    sleep(1)

    make_number = "2"
    
faces = ["wow!", "normal", "smile", "smile_wink", "wink"]

x = -20
for face in faces:
	set_creeper(mc, x=x, block_id="green_wool", face=face)
	mc.postToChat(face)
	x += 10


    



    
