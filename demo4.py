from mcpi import minecraft

def main():
    mc = minecraft.Minecraft.create()

    mc.postToChat('Hello Minecraft World!')


    if __name__ =='__main__':
        main()