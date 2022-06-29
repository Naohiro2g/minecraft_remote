from mcje.minecraft import Minecraft
import param_MCJE as param
import circle as cr
from ms_font import font_design,FONT_HEIGHT,FONT_WIDTH

MASS_HEIGHT = FONT_HEIGHT + 2
MASS_WIDTH = FONT_WIDTH + 4
STA_X = 50
STA_Y = 71
STA_Z = 50


class MCJESweeper():
    def __init__(self, mc):
        self.mass_x = STA_X
        self.mass_z = STA_Z
        self.mc = mc

    def set_cell(self, column=0, row=0):
        self.mc.setBlocks(STA_X + row * 6 - 3, STA_Y, STA_Z + column * 6 - 3,
                          STA_X + row * 6 + 3, STA_Y, STA_Z + column * 6 + 3,
                          param.BLACK_CONCRETE)
        self.mc.setBlocks(STA_X + row * 6 - 2, STA_Y, STA_Z + column * 6 - 2,
                          STA_X + row * 6 + 2, STA_Y, STA_Z + column * 6 + 2,
                          param.STONE)

    def change_color(self,num):
        self.concrete_c = param.CONCRETE
        if num == 1:
            self.concrete_c = param.LIGHT_BLUE_CONCRETE
        elif num == 2:
            self.concrete_c = param.ORANGE_CONCRETE
        elif num == 3:
            self.concrete_c = param.LIME_CONCRETE
        elif num == 4:
            self.concrete_c = param.PINK_CONCRETE
        elif num == 5:
            self.concrete_c = param.YELLOW_CONCRETE
        elif num == 6:
            self.concrete_c = param.LIGHT_GRAY_CONCRETE
        elif num == 7:
            self.concrete_c = param.BROWN_CONCRETE
        elif num == 8:
            self.concrete_c = param.RED_CONCRETE

    def cellOpen(self,j,i):
        self.mass_x = STA_X - j*6
        self.mass_z = STA_Z + i*6
        self.mc.setBlocks(self.mass_x-2,STA_Y,self.mass_z-2,self.mass_x+2,STA_Y,self.mass_z+2,param.CONCRETE)

    def check_mine(self,mine_num,j,i):
        self.change_color(mine_num)
        self.offscreen = []
        rendition = font_design[mine_num]
        line_offset = 0
        for line in rendition:
            if len(self.offscreen) <= line_offset:
                self.offscreen.append([])
            for dot in line:
                if dot == '0':
                    self.offscreen[line_offset].append(self.concrete_c)
                else:
                    self.offscreen[line_offset].append(param.CONCRETE)

        self.draw_num(j,i)

    def draw_num(self,j,i):
        pen_x = STA_X - j*6 + 2
        pen_z = STA_Z + i*6 - 1
        count = 0
        for line in self.offscreen:
            for dot in line:
                self.mc.setBlock(pen_x,STA_Y,pen_z,dot)
                pen_z += 1
                count += 1
                if count == 3:
                    count =0
                    pen_z -= 3
                    pen_x -= 1

    def raiseFrag(self,j,i):
        self.mass_x = STA_X - j*6
        self.mass_z = STA_Z + i*6
        self.mc.setBlocks(self.mass_x-2,STA_Y,self.mass_z-2,self.mass_x+2,STA_Y,self.mass_z+2,param.ORANGE_CONCRETE)

    def dropFrag(self,j,i):
        self.mass_x = STA_X - j*6
        self.mass_z = STA_Z + i*6
        self.mc.setBlocks(self.mass_x-2,STA_Y,self.mass_z-2,self.mass_x+2,STA_Y,self.mass_z+2,param.CONCRETE)

    def game_over(self):
        self.mc.postToChat("YOU LOSE,俺の勝ち、なんで負けたか明日までに考えといてください。ほな頂きます。")


if __name__ == '__main__':
    BOARD_WIDTH, BOARD_HEIGHT = 20, 10
    mc = Minecraft.create(port=param.PORT_MC)
    mjs = MCJESweeper(mc)
    mjs.setMass(BOARD_WIDTH,BOARD_HEIGHT)
    mjs.check_mine(2,0,0)
