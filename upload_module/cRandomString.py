# -*- coding:utf-8 -*-
# author:Kyseng
# file: cRandomString.py
# time: 2018/11/8 11:41 PM
# functhion:
import random

class cRandomString():
    @staticmethod
    def RandomTitle(name):
        platform = ["PS4", "XBOX", "PC", "NS", "IOS"]
        random.shuffle(platform)
        platform = "/".join(platform)


        firstWord = ['Cool', 'Hot', 'New', '2018', 'Gift', '*Cool*', '*Hot*', '*New*', '$Cool$', '$Hot$', '$New$']
        firstWord = random.choice(firstWord)

        title = firstWord + ' 🤑 FREE Fortnite XXXX SKIN ' + platform

        title = title.replace('XXXX', name)

        return title

    @staticmethod
    def RandomDescription(name):
        platform = ["PS4", "Xbox One", "PC", "Nintendo Switch", "IOS"]
        random.shuffle(platform)
        platform = ", ".join(platform)

        description_temp = "Hey Guys!\n\nIn today's video I will show you how to get the XXXX skin for free in fortnite!\n\nThis is working on xbox, ps4, ios, pc and nintendo switch!\n\nThis method is 100% free and working as of 2018.\n\nThis is the best way to get a fortnite XXXX skin for free key code! \n\nThis is a working and legal method!\n\nHow To Get FREE SKINS In Fortnite: Battle Royale! [{0}]".format(platform)

        description_final = description_temp.replace('XXXX', name)

        return description_final

    @staticmethod
    def RandomTag(name):
        tag_temp = "XXXX, XXXX fortnite, XXXX free, XXXX skin,fortnite XXXX skin free, how to get the XXXX skin, iPhone XXXX free skins, iPad XXXX free skins"
        tag_final = tag_temp.replace('XXXX', name)

        return tag_final

if __name__ == "__main__":
    cRandomString.RandomDescription("123")