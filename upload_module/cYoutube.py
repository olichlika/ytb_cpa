# -*- coding:utf-8 -*-
# author:Kyseng
# file: cYoutube.py
# time: 2018/11/13 12:48 AM
# functhion:
from oauth2client.client import flow_from_clientsecrets
import os
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import httplib2
import argparse
from cRandomString import cRandomString
import time
import random
import httplib

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
                        httplib.IncompleteRead, httplib.ImproperConnectionState,
                        httplib.CannotSendRequest, httplib.CannotSendHeader,
                        httplib.ResponseNotReady, httplib.BadStatusLine)

MAX_RETRIES = 10

class cYoutube():
    def __init__(self, oauth):
        self.oauth = oauth
        # 获取授权
        self.youtube = self.get_authenticated_service()

    def get_authenticated_service(self):
        self.homedir = os.path.dirname(__file__)
        self.oauthdir = os.path.join(self.homedir, 'oauth')

        CLIENT_SECRETS_FILE = os.path.join(self.homedir, 'client_secret.json')
        YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
        MISSING_CLIENT_SECRETS_MESSAGE = ""
        flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE, message=MISSING_CLIENT_SECRETS_MESSAGE)

        oauth_path = os.path.join(self.oauthdir, self.oauth)
        # print oauth_path
        storage = Storage(oauth_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"

        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def initialize_upload(self, youtube, options):
        tags = None
        if options.keywords:
            tags = options.keywords.split(',')

        body = dict(
            snippet=dict(
                title=options.title,
                description=options.description,
                tags=tags,
                categoryId=options.category
            ),
            status=dict(
                privacyStatus=options.privacyStatus
            )
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            # The chunksize parameter specifies the size of each chunk of data, in
            # bytes, that will be uploaded at a time. Set a higher value for
            # reliable connections as fewer chunks lead to faster uploads. Set a lower
            # value for better recovery on less reliable connections.
            #
            # Setting 'chunksize' equal to -1 in the code below means that the entire
            # file will be uploaded in a single HTTP request. (If the upload fails,
            # it will still be retried where it left off.) This is usually a best
            # practice, but if you're using Python older than 2.6 or if you're
            # running on App Engine, you should set the chunksize to something like
            # 1024 * 1024 (1 megabyte).
            media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
        )

        video_id = self.resumable_upload(insert_request)
        return video_id

    def resumable_upload(self, request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print 'Uploading file...'
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print 'Video id "%s" was successfully uploaded.' % response['id']
                        return response['id']
                    else:
                        exit('The upload failed with an unexpected response: %s' % response)
            except HttpError, e:
                if e.resp.status in RETRIABLE_STATUS_CODES:
                    error = 'A retriable HTTP error %d occurred:\n%s' % (e.resp.status,
                                                                         e.content)
                else:
                    raise
            except RETRIABLE_EXCEPTIONS, e:
                error = 'A retriable error occurred: %s' % e

            if error is not None:
                print error
                retry += 1
                if retry > MAX_RETRIES:
                    exit('No longer attempting to retry.')

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print 'Sleeping %f seconds and then retrying...' % sleep_seconds
                time.sleep(sleep_seconds)

    def upload_video(self, file, name):
        VALID_PRIVACY_STATUSES = ('public', 'private', 'unlisted')

        parser = argparse.ArgumentParser()
        parser.add_argument('--file', required=False, help='Video file to upload')
        parser.add_argument('--title', help='Video title', default='Test Title')
        parser.add_argument('--description', help='Video description',
                            default='Test Description')
        parser.add_argument('--category', default='22',
                            help='Numeric video category. ' +
                                 'See https://developers.google.com/youtube/v3/docs/videoCategories/list')
        parser.add_argument('--keywords', help='Video keywords, comma separated',
                            default='')
        parser.add_argument('--privacyStatus', choices=VALID_PRIVACY_STATUSES,
                            default='private', help='Video privacy status.')
        args = parser.parse_args()

        # title_temp = '🤑 FREE Fortnite XXXX SKIN PS4/XBOX/PC/NS/iOS'
        # title_final = title_temp.replace('XXXX', title)
        #
        # description_temp = "Hey Guys!\n\nIn today's video I will show you how to get the XXXX skin for free in fortnite! This is working on xbox, ps4, ios, pc and nintendo switch!\n\nThis method is 100% free and working as of 2018. This is the best way to get a fortnite XXXX skin for free key code! This is a working and legal method!\n\nHow To Get FREE SKINS In Fortnite: Battle Royale! [PS4, Xbox One, PC, NS, iOS, Nintendo Switch]"
        # description_final = description_temp.replace('XXXX', title)
        #
        # tag_temp = "XXXX, XXXX fortnite, XXXX free, XXXX skin,fortnite XXXX skin free, how to get the XXXX skin, iPhone XXXX free skins, iPad XXXX free skins"
        # tag_final = tag_temp.replace('XXXX', title)

        args.file = file
        args.title = cRandomString.RandomTitle(name)
        args.description = cRandomString.RandomDescription(name)
        args.category = '20'
        args.keywords = cRandomString.RandomTag(name)
        args.privacyStatus = 'public'

        try:
            video_id = self.initialize_upload(self.youtube, args)
            return video_id
        except HttpError, e:
          print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)


    def upload_thumbnail(self, video_id, file):
        self.youtube.thumbnails().set(
            videoId=video_id,
            media_body=file
        ).execute()

    def Upload_thumbnail(self, video_id, file):
        try:
            self.upload_thumbnail(video_id, file)
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
        else:
            print "The custom thumbnail was successfully set."