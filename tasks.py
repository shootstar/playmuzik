#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import pyechonest
import soundcloud
import urllib2
from celery import Celery


from audio import LocalAudioFile
from models import save_to_database
try:
    import settings
except:
    import sample_settings as settings

pyechonest.config.ECHO_NEST_API_KEY = os.environ.get("ECHO_NEST_API_KEY",settings.ECHO_NEST_API_KEY)
SOUNDCLOUD_CLIENT_KEY = os.environ.get("SOUNDCLOUD_CLIENT_KEY",settings.SOUNDCLOUD_CLIENT_KEY)
soundcloud_client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_KEY)

celery = Celery('tasks', broker='amqp://guest@localhost//')

def analyse_muzik(filename=None):
    data = LocalAudioFile(filename)
    return data

def generate_filename():
   timestamp = time.time()
   return "".join(str(timestamp).split(".")) + ".mp3"

@celery.task
def get_soundcloud_muzik(sound_url):
    print "helllo"
    s = soundcloud_client.get("/resolve",url=sound_url)
    if s.downloadable and s.original_format == "mp3":
        url = s.download_url
    else:
        url = s.stream_url


    url += "?client_id=" + settings.SOUNDCLOUD_CLIENT_KEY
    result = urllib2.urlopen(url)
    name = s.title
    artist = s.user.get("username")
    filename = settings.SOUNDCLOUD_PATH + generate_filename()
    with open(filename,"w") as f: #TODO raw mp3 possible to analyse
        f.write(result.read())
    data = analyse_muzik(filename)
    result = save_to_database(name,artist,url,data)

    return result

# @celery.task
# def get_youtube_muzik(url):
#     value = ""
#     artist = None
#
#     filepath = compat_str(settings.YOUTUBE_PATH + generate_filename())
#     y = YoutubeDL({"format":"18/34/35/5/17","outtmpl":filepath})
#     y.add_default_info_extractors()
#     y.add_post_processor(FFmpegExtractAudioPP(preferredcodec="mp3"))
#     value = y.download([url])
#
#     name = get_youtube_title(url)
#     data = analyse_muzik(filepath)
#     result = save_to_database(name,artist,url,data)
#     return result