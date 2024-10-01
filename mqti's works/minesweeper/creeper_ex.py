import math
import numpy
from time import sleep
from mcje.minecraft import Minecraft
import param_MCJE as param
FACE_FLAME = 8
POSITIVE = 1
NEGATIVE = -1
second = 3
#デザインを追加、変更することで顔を変えることができます!
#You can add or change designs.And Creeper smiles with different face!
creeper_design = [
    '        ',
    '        ',
    ' 00  00 ',
    ' 00  00 ',
    '   00   ',
    '  0000  ',
    '  0000  ',
    '  0  0  ',
]

print("creeper_ex loaded!!")
    
def creeper_set(mc,x,y,z,var='x',neg='y',code=POSITIVE,core={},head_block=param.LIME_GLASS,parts_block=param.COAL_BLOCK):
    if core == {}:
        cube_core = get_core(x,y,z)
    else:
        cube_core = core
    if var == 'x' and neg == 'y' or var == 'y' and neg == 'x':
        Zlength = numpy.sign(cube_core['z'] - z)*(FACE_FLAME-1)
    elif var == 'z' and neg == 'y' or var == 'y' and neg == 'z':
        Xlength = numpy.sign(cube_core['x'] - x)*(FACE_FLAME-1)
    elif var == 'x' and neg == 'z' or var == 'z' and neg == 'x':
        Ylength = numpy.sign(cube_core['y'] - y)*(FACE_FLAME-1)
    line_offset = 0 ; once = True
    Ax,Ay,Az = x,y,z
    for line in creeper_design:
        dot_offset = 0
        for dot in line:
            if dot == '0':
                block_color_id = parts_block
            else:
                block_color_id = head_block
            
            if var == 'x':
                Ax = x + dot_offset*code
                Xlength = (FACE_FLAME-1)*code
            if var == 'y':
                Ay = y + dot_offset*code
                Ylength = (FACE_FLAME-1)*code
            if var == 'z':
                Az = z + dot_offset*code
                Zlength = (FACE_FLAME-1)*code
            
            if neg == 'x':
                Ax = x - line_offset
                Xlength = -FACE_FLAME+1
            if neg == 'y':
                Ay = y - line_offset
                Ylength = -FACE_FLAME+1
            if neg == 'z':
                Az = z - line_offset
                Zlength = -FACE_FLAME+1
            if once == True:
                mc.setBlocks(x,y,z,x + Xlength,y + Ylength,z + Zlength,head_block)
                once = False
            mc.setBlock(Ax,Ay,Az,block_color_id)
            dot_offset += 1
        line_offset += 1
    sleep(second)
    mc.setBlocks(x,y,z,x + Xlength,y + Ylength,z + Zlength,param.AIR)

def get_core(x,y,z):
    return {'x':x + math.ceil(FACE_FLAME/2),
            'y':y - math.ceil(FACE_FLAME/2),
            'z':z - math.ceil(FACE_FLAME/2),}

def creeper_turn(mc,x,y,z):
    cube_core = get_core(x,y,z)
    mc.postToChat("x -> ~"+str(FACE_FLAME)+",y -> ~-"+str(FACE_FLAME)+",z -> ~"+str(FACE_FLAME)+", "+str(FACE_FLAME)+"^3 cube")
    Ax = x ; Ay = y ; Az = z
    creeper_set(mc,Ax,Ay,Az,'x','y',POSITIVE,cube_core)
    Ax += (FACE_FLAME-1)
    creeper_set(mc,Ax,Ay,Az,'z','y',NEGATIVE,cube_core)
    Az -= (FACE_FLAME-1)
    creeper_set(mc,Ax,Ay,Az,'x','y',NEGATIVE,cube_core)
    Ax -= (FACE_FLAME-1)
    creeper_set(mc,Ax,Ay,Az,'z','y',POSITIVE,cube_core)
    Ax += (FACE_FLAME-1)
    creeper_set(mc,Ax,Ay,Az,'z','x',POSITIVE,cube_core) 
    Ay -= (FACE_FLAME-1) ; Az += (FACE_FLAME-1)
    creeper_set(mc,Ax,Ay,Az,'x','z',NEGATIVE,cube_core)

if __name__ == '__main__':
    mc = Minecraft.create(port=param.PORT_MC)
    creeper_set(mc,0,80,0)
    creeper_turn(mc,0,80,0)