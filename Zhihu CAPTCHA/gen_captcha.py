# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np
import random
import math, string
import logging


# logger = logging.Logger(name='gen verification')

class RandomChar():
    @staticmethod
    def Unicode():
        val = random.randint(0x4E00, 0x9FBF)
        return chr(val)

    @staticmethod
    def GB2312():
        head = random.randint(0xB0, 0xCF)
        body = random.randint(0xA, 0xF)
        if (body == 0xA):
            tail = random.randint(0x1, 0xF)
        else:
            if (body == 0xF):
                tail = random.randint(0, 0xE)
            else:
                tail = random.randint(0, 0xF)
        val = bytes([head, (body << 4) + tail])
        # print(val)

        return val.decode('gb2312')


class ImageChar():
    def __init__(self, fontColor=(0, 0, 0),
                 size=(1000, 400),
                 fontPath='./Kai.ttf',
                 bgColor=(255, 255, 255, 255),
                 fontSize=200):
        self.size = size
        self.fontPath = fontPath
        self.bgColor = bgColor
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = ImageFont.truetype(self.fontPath, self.fontSize)
        self.image = Image.new('RGBA', size, bgColor)
    def drawText(self, pos, txt, fill, flip):

        image = Image.new('RGBA', (self.fontSize+10,self.fontSize+10), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        draw.text((0,0), txt, font=self.font, fill=fill)

        if (flip == False):
            w = image
        else:
            w = ImageOps.flip(image)


        # bias = 0
        bias = random.randrange(-10, 10)
        w = w.rotate(bias, expand=1)
        # w.show()
        # self.image.show()
        # self.image = Image.alpha_composite(self.image, w)
        self.image.paste(w, pos, w)

    def randRGB(self):
        return self.fontColor

    def randChinese(self, num, num_flip):
        gap = random.randint(-65,-45)
        start = (self.size[0] - (num * (self.fontSize + gap) - gap)) // 2
        num_flip_list = random.sample(range(num), num_flip)
        # logger.info('num flip list:{0}'.format(num_flip_list))
        # print('num flip list:{0}'.format(num_flip_list))
        char_list = []
        y = (self.size[1] - self.fontSize)
        for i in range(0, num):
            char = RandomChar().GB2312()
            char_list.append(char)
            x = start + self.fontSize * i + gap + gap * i

            if i in num_flip_list:
                self.drawText((x, y), char, self.randRGB(), flip=True)
            else:
                self.drawText((x, y), char, self.randRGB(), flip=False)

        return char_list, num_flip_list

    def save(self, path):
        self.image.save(path)

    def show(self):
        self.image.show()


err_num = 0
for i in range(10000):
    ic = ImageChar(fontColor=(80, 80, 80, 255), size=(1800, 300), fontSize=250)
    num_flip = random.randint(1, 4)
    char_list, num_flip_list = ic.randChinese(7, num_flip)

    # ic.show()
    save_path = './train_data/' + ''.join(char_list) + '_' + ''.join((str(i) for i in num_flip_list)) + ".png"
    # print(save_path)
    ic.save(save_path)
