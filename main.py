# -*- coding:utf-8 -*-
# author:Kyseng
# file: main.py
# time: 2018/11/12 9:28 PM
# functhion:
import threading
import os
import time
import signal
import sys
from upload_module.cUpload import cUpload
from crawl_module.cFortniteSpider import cFortniteSpider

def crawl():
    while 1:
        print "开始爬取新皮肤"
        cFortniteSpider.run()
        time.sleep(24 * 60 * 60) #休息24小时


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
            cUpload(oauth_file).upload(10) #上传10个

        time.sleep(10) #休息10秒

def quit(signum, frame):
    print 'You choose to stop me.'
    sys.exit()

def run():
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)

        a = threading.Thread(target = upload)

        b = threading.Thread(target = crawl)

        a.setDaemon(True)
        a.start()

        b.setDaemon(True)
        b.start()

        while True:
            pass
    except Exception, exc:
        print exc

if __name__ == "__main__":
    run()