import cv2
import sys
import param_MCJE as param
from mcje.minecraft import Minecraft
from time import sleep

STA_X = 0 ; STA_Y = 80 ; STA_Z = 0

def badapple():
    filename = './images/badapple.avi'
    video = cv2.VideoCapture(filename)
    if not video.isOpened():
        print("Could not open video")
        sys.exit()
    ok,frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    mc = Minecraft.create(port=param.PORT_MC)
    img_array = [[-1] * 80 for _ in range(60)]
    succeed = False
    while True:
        ok,frame = video.read()
        if(ok):
            succeed = True
            img = cv2.resize(frame,(80,60))
            line_offset = 0
            for line in img:
                dot_offset = 0
                for dot in line:
                    if dot[0] <= 130:
                        if not img_array[line_offset][dot_offset] == 1:
                            mc.setBlock(STA_X + dot_offset,STA_Y,STA_Z + line_offset,param.BLACK_CONCRETE)
                            img_array[line_offset][dot_offset] = 1
                    else:
                        if not img_array[line_offset][dot_offset] == 0:
                            mc.setBlock(STA_X + dot_offset,STA_Y,STA_Z + line_offset,param.CONCRETE)
                            img_array[line_offset][dot_offset] = 0    
                    dot_offset += 1
                line_offset += 1
            sleep(1/60)
        else:
            if succeed == True:
                print("worked GOOD")
            else:
                print("got ERROR")
            break

badapple()