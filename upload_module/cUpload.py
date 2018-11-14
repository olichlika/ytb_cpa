# -*- coding:utf-8 -*-
# author:Kyseng
# file: cYoutube.py
# time: 2018/11/12 3:31 PM
# functhion:
import mysql
import random
from cCover.cCover import cCover
from cFFmpeg.cFFmpeg import cFFmpeg
from cYoutube import cYoutube

class cUpload(object):
    def __init__(self, oauth): #传入的oauth是文件名
        self.oauth = oauth
        # self.upload_num = upload_num

    def upload(self, upload_num):
        mUpload = cYoutube(self.oauth)  # 上传授权
        db = mysql.DBPipeline()

        data = db.getSkin(self.oauth) #获取可上传的数据
        if data != None:
            sample_data = random.sample(data, upload_num) #随机挑选upload_num个上传
            for d in sample_data:
                skinName = d[1]
                skinURL = d[2]

                # print skinName, skinURL

                #制作封面
                cover = cCover(skinURL, 1280, 720, 'EN').makeCoverPic()
                print cover

                #制作上传视频
                video = cFFmpeg(skinName).run()
                print video

                #开始上传
                video_id = mUpload.upload_video(video, skinName)

                #上传封面
                mUpload.Upload_thumbnail(video_id, cover)

                #成功插入数据库
                db.insert_new_row(self.oauth, skinName)




if __name__ == "__main__":
    x = cUpload('oauth0.json')
    x.upload(1)



