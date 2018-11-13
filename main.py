# -*- coding:utf-8 -*-
# author:Kyseng
# file: main.py
# time: 2018/11/12 9:28 PM
# functhion:
import threading
import os
import time
from upload_module.cUpload import cUpload

def crawl():
    while 1:
        print "开始爬取新皮肤"
        time.sleep(15) #休息24小时


def upload():
    while 1:
        #读取授权文件
        homedir = os.getcwd()
        ytbdir = os.path.join(homedir, 'upload_module')
        oauthdir = os.path.join(ytbdir, 'oauth')

        oauth_files_list = os.listdir(oauthdir)

        for oauth_file in oauth_files_list:
            print "正在上传:" + oauth_file
            #查询返回fortnite_skin_table表不包含在fortnite_skin_ytb_table中的字段
            # cUpload(oauth_file).upload(10)
        time.sleep(10) #休息10秒

def a():
    while 1:
        print 1111
        time.sleep(1)
def b():
    while 1:
        print 2222
        time.sleep(3)

def run():
    threads = []
    t = threading.Thread(target = upload)
    threads.append(t)

    t = threading.Thread(target = crawl)
    threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    run()