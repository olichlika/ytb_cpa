# -*- coding:utf-8 -*-
# author:Kyseng
# file: cFFmpeg.py
# time: 2018/11/8 11:59 PM
# functhion:
import os
import shutil
from ffmpy import FFmpeg
import random

class cFFmpeg():

    def __init__(self, game_name):
        self.game_name = game_name

        self.homedir = os.path.dirname(__file__)
        self.tmpdir = os.path.join(self.homedir, 'tmp')

        shutil.rmtree(self.tmpdir)  # 清空文件夹
        os.mkdir(self.tmpdir)

    #生成字幕
    def makeSRT(self):
        path = os.path.join(self.tmpdir, 'subtitle.srt')
        file = open(path, 'wb')
        subtitle_str = '1\n00:00:40,00 --> 00:00:50,00\nSelect ' + self.game_name
        file.write(subtitle_str)
        file.close()
        return path

    #插入字幕
    def insertSRT(self, video_path, srt):
        # templet_file = os.path.join(self.homedir, 'templet.mp4')
        out_file = os.path.join(self.tmpdir, 'mid.mp4')

        ff = FFmpeg(
            inputs={'{0}'.format(video_path): None},
            outputs={
                '{0}'.format(out_file): "-vf subtitles={0}:force_style='Fontsize=22' -max_muxing_queue_size 9000 -c:a copy -y".format(srt)
            }
        )
        ff.run()
        return out_file

    #加入水印
    def insertTextWatermark(self, video_path, text):
        result_file = os.path.join(self.tmpdir, 'result.mp4')

        x = random.randint(1, 1100)
        y = random.randint(1, 650)
        fontfile = os.path.join(self.homedir, 'wryh.ttf')
        ff = FFmpeg(
            inputs={'{0}'.format(video_path): None},
            outputs={
                '{0}'.format(
                    result_file): "-vf drawtext=fontfile={3}:text=\'{2}\':x={0}:y={1}:fontsize=24:fontcolor=black:alpha=0.1 -y".format(x, y, text, fontfile)
            }
        )
        ff.run()
        return result_file

    def run(self):
        srt = self.makeSRT()
        temple = os.path.join(self.homedir, 'templet.mp4')
        mid = self.insertSRT(temple, srt)
        r = self.insertTextWatermark(mid, "www.freeskin.club")
        return r

if __name__ == "__main__":
    x = cFFmpeg("xxoo").run()
    print x