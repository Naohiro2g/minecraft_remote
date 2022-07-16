from mcje.minecraft import Minecraft
import param_MCJE1122 as param


mc = Minecraft.create(port=param.PORT_MC)
mc.postToChat("接続完了")


def make_house(X=0, Y=3, Z=0, material=param.DIAMOND_BLOCK):
    # スーパーフラット用なので普通の世界で作成するときはY座標をいじってください
    mc.setBlocks(X,     Y,     Z,     X - 5, Y + 5, Z + 5, material)
    mc.setBlocks(X - 1, Y + 1, Z + 1, X - 4, Y + 4, Z + 4, param.AIR)
    mc.setBlocks(X,     Y + 1, Z + 4, X,     Y + 2, Z + 4, param.AIR)

    mc.setBlocks(X,     Y + 2, Z + 2,  X, Y + 3, Z + 1, param.GLASS)

    mc.setBlock(X - 4, Y + 1, Z + 5, 58)  # crafting_table


make_house(X=7)
