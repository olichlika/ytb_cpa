# -*- coding:utf-8 -*-
# author:Kyseng
# file: cCover.py
# time: 2018/11/8 1:11 AM
# functhion:
import os
import urllib2
import random
from random import Random
import shutil
import colorsys
from PIL import Image, ImageDraw, ImageFont

class cCover():

    def __init__(self, url, width, height, language):
        self.url = url
        self.thumb_width = width
        self.thumb_height = height
        self.language = language

        self.homedir = os.path.dirname(__file__)
        self.tmpdir = os.path.join(self.homedir, 'tmp')

        files_list = os.listdir(self.tmpdir)
        if(len(files_list) > 300):
            shutil.rmtree(self.tmpdir) #清空文件夹
            os.mkdir(self.tmpdir)

    def randomName(self, randomlength=16):
        str = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(randomlength):
            str += chars[random.randint(0, length)]
        return str

    def saveImg(self, url):
        ext = url.split('.')[-1]
        # print ext
        name = self.randomName() + '.' + ext
        path = os.path.join(self.tmpdir, name)
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
        }
        request = urllib2.Request(url, None, header)
        response = urllib2.urlopen(request).read()
        f = file(path, "wb")
        f.write(response)
        f.close()
        return path

    def get_dominant_color(self, image):

        # 颜色模式转换，以便输出rgb颜色值
        image = image.convert('RGBA')

        # 生成缩略图，减少计算量，减小cpu压力
        image.thumbnail((200, 200))

        max_score = 0
        dominant_color = 0

        for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
            # 跳过纯黑色
            if a == 0:
                continue

            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

            y = (y - 16.0) / (235 - 16)

            # 忽略高亮色
            if y > 0.9:
                continue

            # Calculate the score, preferring highly saturated colors.
            # Add 0.1 to the saturation so we don't completely ignore grayscale
            # colors by multiplying the count by zero, but still give them a low
            # weight.
            score = (saturation + 0.1) * count

            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)

        return dominant_color

    def rand_rgb(self):
        '''Generate a random rgb color.'''
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def makeCoverPic(self):
        img_path = self.saveImg(self.url)

        #制作背景图片
        fill_color = self.get_dominant_color(Image.open(img_path))
        bk_img = Image.new("RGB", (self.thumb_width, self.thumb_height), fill_color) #生成的背景图片
        # bk_img = bk_img.convert('RGBA')

        #缩放原始图片
        img = Image.open(img_path)
        img = img.convert('RGBA') #转换
        img_width = img.size[0]
        img_height = img.size[1]
        if img_height != self.thumb_height:
            scale = 1.0 * img_width / img_height
            new_img_height = self.thumb_height
            new_img_width = int(new_img_height * scale)
            resized_img = img.resize((new_img_width, new_img_height), Image.LINEAR)
        else:
            resized_img = img #不变

        #两张图片重合
        img_w, img_h = resized_img.size
        bg_w, bg_h = bk_img.size
        offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
        bk_img.paste(resized_img, offset, mask = resized_img)

        #添加字幕
        if self.language == "EN":
            line1 = "FREE SKINS"
            line2 = "PS4/XBOX/NS/PC/iOS"
        else:
            return

        font_path = os.path.join(self.homedir, 'ArialBlack.ttf')

        draw = ImageDraw.Draw(bk_img)
        ttfont = ImageFont.truetype(font_path, 170)
        f_w, f_h = ttfont.getsize(line1) #获取line1的长宽
        mid_x = (bg_w - f_w) / 2
        mid_y = (bg_h - f_h) / 2
        # print mid_x, mid_y
        draw.text((mid_x, mid_y), line1, fill=self.rand_rgb(), font=ttfont)
        ttfont = ImageFont.truetype(font_path, 100)
        f_w, f_h = ttfont.getsize(line2) #获取line2的长宽
        mid_x = (bg_w - f_w) / 2
        mid_y = (bg_h - f_h) / 2
        # print mid_x, mid_y
        draw.text((mid_x, mid_y + 170), line2, fill=self.rand_rgb(), font=ttfont)
        # print ttfont.getsize(line2)
        # bk_img.show()

        # 保存图片
        name = self.randomName() + '.jpg'
        path = os.path.join(self.tmpdir, name)
        bk_img.save(path, 'JPEG', quality = 120)

        return path

if __name__ == "__main__":
    x = cCover("https://skin-tracker.com/images/fnskins/561.png", 1280, 720, 'EN').makeCoverPic()

    # template_image = "/Volumes/Hack/python/ytb_cpa_v1/upload_module/cCover/tmp/pic/UKjeRJxzYFc1RJic.png"
    # template = Image.open(template_image)
    # a_band = template.split()[-1]
    # print a_band
    # # 拿到图片的尺寸
    # template_size = template.size
    # print template_size[0], template_size[1]