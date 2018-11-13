# -*- coding:utf-8 -*-
# author:Kyseng
# file: spider.py
# time: 2018/11/9 10:58 AM
# functhion:
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import mysql

class cFortniteSpider():
    @staticmethod
    def run():
        db = mysql.DBPipeline()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/527.36",
        }
        session = requests.session()

        url = "https://skin-tracker.com/fortnite/skins?rarity=1&sort=3&limit=3"
        result = session.get(url=url, headers=headers).content
        result = BeautifulSoup(result, 'html.parser')
        # print result

        # driver = webdriver.PhantomJS()
        # driver.get(url)
        # print (driver.page_source)

        #
        # result = BeautifulSoup(driver.page_source, 'xml')
        # print result
        # 获取图片
        figures = result.find_all('figure', attrs={"class": "skincard"})
        # print len(figures)
        for f in figures:
            imgs = f.find('div', attrs={"class": "image"}).find_all('img')
            if len(imgs) == 2:
                img = imgs[1]
            elif len(imgs) == 1:
                img = imgs[0]

            img_url = img.attrs['src'].replace(' ', '').replace('\n', '').replace('\r\n', '')
            if "https://" not in img_url:
                img_url = "https://skin-tracker.com" + img_url

            skin_name = img.attrs['alt'].replace(' icon','')
            if "Crazy Feet Emote" not in skin_name:
                status = db.check_exist(skin_name)  # 判断是否需要保存
                if status == 'noexist':  # 不存在 存入
                    db.insert_new_row(skin_name, img_url)

if __name__ == "__main__":
    cFortniteSpider.run()
