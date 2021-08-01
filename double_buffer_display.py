"""
Class BufferDisplay
"""

# Minecraft Java Edition 1.16.5
# import param_MCJE as param

# Minecraft Java Edition 1.12.2
# import param_MCJE1122 as param

# Minecraft Pi Edition
import param_MCPI as param

from font_5x7 import font_design, FONT_WIDTH, FONT_HEIGHT


# display frame
DISP_HEIGHT = FONT_HEIGHT + 4
BLOCK_FRAME = param.GOLD_BLOCK
LETTER_SPACING = 1

class BufferDisplay():
    """
    Double-buffer display for voxel letters in the Minecraft world.
    update(): render and flip
    render(): drawing on off-screen buffer
    flip(): copy only changes from off-screen to on-screen and Minecraft world
    delete(): delete display frame and contents
    """

    def __init__(self,
                mc,
                anchor_position=(0,param.Y_SEA + 20,0),
                block_frame=param.GOLD_BLOCK,
                num_of_letters=12):
        """
        Set everything up to render messages on the display frame
        with the given anchor or starting position.
        anchor is at the topleft of the display frame.
        """
        self.mc = mc
        self.anchor_position = anchor_position
        self.block_frame = block_frame
        self.num_of_letters = num_of_letters
        self.clear()

    def update(self, message, block_letters=param.GOLD_BLOCK):
        self.render(message, block_letters=block_letters)
        self.flip()

    def render(self, message, block_letters=param.GOLD_BLOCK):
        """
        Put the message into the off-screen buffer.
        Do nothing if the message has not changed from the last time.
        """
        if message != self.last_message:  # Do nothing if the message has not changed.
            self.last_message = message   # Save for the next time.

            self.offscreen = []  # Clear the buffer.
            letter_offset = 0
            for letter in message:
                rendition = font_design[letter]
                line_offset = 0
                for line in rendition:
                    if len(self.offscreen) <= line_offset:
                        # Make space to store the drawing.
                        self.offscreen.append([])
                    dot_offset = 0
                    for dot in line:
                        if dot == '0':  # on
                            self.offscreen[line_offset].append(block_letters)
                        else:           # off
                            self.offscreen[line_offset].append(param.AIR)
                        dot_offset += 1
                    for _blank in range(dot_offset, FONT_WIDTH + LETTER_SPACING):
                        # Expand short lines to the full width.
                        self.offscreen[line_offset].append(param.AIR)
                    line_offset += 1
                letter_offset += 1

    def flip(self):
        """
        Put the off-screen buffer onto the screen.
        Send only changes from off-screen to on-screen and Minecraft world
        """
        line_offset = 0
        for line in self.offscreen:
            dot_offset = 0
            for dot in line:  # check off-screen dot by dot
                # if on-screen is changed from off-screen
                #     on-screen <- dot
                #     place the dot in MC world by setBlock
                if self.onscreen[line_offset][dot_offset] != dot:
                    self.onscreen[line_offset][dot_offset] = dot
                    self.mc.setBlock(
                            self.anchor_position[0] + 2 + dot_offset,
                            self.anchor_position[1] - 2 - line_offset,
                            self.anchor_position[2],
                            dot)
                dot_offset += 1
            line_offset += 1

    def clear(self):
        """
        Prepare the on-screen buffer and refresh display frame
        """
        # Create buffers and fill on screen buffer with AIR voxels
        self.last_message = ''
        self.offscreen = []
        self.onscreen = []
        line_offset = 0
        for _line in range(FONT_HEIGHT):
            self.onscreen.append([])
            for _dot in range((FONT_WIDTH + LETTER_SPACING) * self.num_of_letters):
                self.onscreen[line_offset].append(param.AIR)
            line_offset += 1
        # Redraw display frame
        x, y, z = self.anchor_position  # topleft of the display frame
        x1 = x + (FONT_WIDTH + LETTER_SPACING) * self.num_of_letters + 2
        y1 = y - DISP_HEIGHT + 1
        self.mc.setBlocks(x,     y,     z,    x1,     y1,     z,  self.block_frame)
        self.mc.setBlocks(x + 1, y - 1, z,    x1 - 1, y1 + 1, z,  param.AIR)

    def delete(self):
        x, y, z = self.anchor_position  # topleft of the display frame
        x1 = x + (FONT_WIDTH + LETTER_SPACING) * self.num_of_letters + 2
        y1 = y - DISP_HEIGHT + 1
        self.mc.setBlocks(x,     y,     z,    x1,     y1,     z,  param.AIR)
