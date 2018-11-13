# -*- coding:utf-8 -*-
# author:Kyseng
# file: getOAUTH.py
# time: 2018/11/12 3:29 PM
# functhion: 生成授权
from oauth2client.client import flow_from_clientsecrets
import os
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

def run():
    homedir = os.getcwd()
    ytbdir = os.path.join(homedir, 'upload_module')
    oauthdir = os.path.join(ytbdir, 'oauth')

    CLIENT_SECRETS_FILE = os.path.join(ytbdir, 'client_secret.json')
    YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
    MISSING_CLIENT_SECRETS_MESSAGE = ""
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)

    # storage = Storage(homedir + '/oauth2.json')
    num = 2
    for i in range(0, num):
        path = os.path.join(oauthdir, 'oauth' + str(i) + '.json')
        storage = Storage(path)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)


if __name__ == "__main__":
    run()