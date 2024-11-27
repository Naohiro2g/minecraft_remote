'''
このプログラムは自由に利用してもらって構いません。
「convert2mc」がapi、つまり本体です。
mcpcを起動すると、操作の仕方みたいなのが簡単にですが分かります。
Verticalは不安定なので、Horizonalを推奨しておきます。
Author: MqtiSub
'''

from mcje.minecraft import Minecraft
import h5py
import numpy as np
from PIL import Image
import os
import tkinter as tk
import tkinter.filedialog as tkf
import re

class mcpc():
    def __init__(self):
        # Connecting To Minecraft...
        mc = Minecraft.create(port=14712)
        root = tk.Tk() ; root.geometry('0x0') ; root.overrideredirect(1)
        root.update() ; root.lift() ; root.focus_force
        fTyp = [("img","*png"),("","*jpg")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        path = tkf.askopenfilename(filetypes = fTyp,initialdir = iDir)
        root.update()
        img = Image.open(path)
        print('loaded: '+path.split('/')[-1]+', size: '+str(img.size[0])+', '+str(img.size[1]))
        _input = [int(re.sub(r'\D+','', input('Magnification?: (%) '))),
                  input('Horizonal or Vertical?: h/v '),
                  re.findall(r'\d+', input('Coordinate?: x, y, z '))]
        img.resize((int(img.size[0]*_input[0]*0.01), int(img.size[1]*_input[0]*0.01))).save('tmp.png')
        mode = 't' if _input[1] == 'h' else 's'
        self.convert2mc('tmp.png', mc, int(_input[2][0]),  int(_input[2][1]), int(_input[2][2]), mode)
        if input('Do you wanna save tmp.png?: y/n ') == 'n': os.remove('tmp.png')  
    @staticmethod
    def convert2mc(path, mc, x, y, z, mode='t'):
        img = Image.open(path)
        if mode == 't' : mc.setBlocks(x, y-1, z, x+img.size[0], y-1, z+img.size[1], 'white_concrete')
        with h5py.File('mc_color.hdf5', mode='r') as f:
            if mode == 's':
                sarr = [f['/side_block/'+i][:] for i in f['/side_block']]
            else:
                sarr = [f['/top_block/'+i][:] for i in f['/top_block']]
            # Combine Top(or Side) and Default.   
            arr = [f['/default_block/'+i][:] for i in f['/default_block']] + sarr
            # I hate that hdf5's keys are iter :/
            default_keys = [k for k in f['/default_block'].keys()]
            top_keys     = [k for k in f['/top_block'].keys()]
            side_keys    = [k for k in f['/side_block'].keys()]
        for column in range(img.size[0]):
            for row in range(img.size[1]):
                ori = np.array(img.getpixel((column, row)))
                # Convert RGBA To RGB.
                if ori.shape == (4,):
                    ori = ori[:3]
                # Get The Vector Margins.
                gap = np.array([((ori - i)**2).sum() for i in arr])
                min_index = gap.argmin()
                # Render in Minecraft.
                block_id = default_keys[min_index] if min_index < 253 else side_keys[min_index-253] if mode == 's' else top_keys[min_index-253]
                if mode == 't':
                    mc.setBlock(x+column, y, z+row, block_id)
                else:
                    mc.setBlock(x+column, y-row-1, z, 'white_concrete')
                    mc.setBlock(x+column, y-row, z, block_id)

if __name__ == '__main__':
    mcpc()