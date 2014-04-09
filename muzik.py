import os
import sys
import time
import shutil
import simplejson
import urlparse
import urllib2
from datetime import datetime

from celery import Celery
from flask import Flask, render_template, request, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


import soundcloud
import pyechonest
import gdata
from echonest.remix.audio import LocalAudioFile
from youtube_dl import YoutubeDL
from youtube_dl.postprocessor import FFmpegExtractAudioPP
from youtube_dl.utils import compat_str

import settings #TODO settings


pyechonest.config.ECHO_NEST_API_KEY = os.environ.get("ECHO_NEST_API_KEY",settings.ECHO_NEST_API_KEY)
SOUNDCLOUD_CLIENT_KEY = os.environ.get("SOUNDCLOUD_CLIENT_KEY",settings.SOUNDCLOUD_CLIENT_KEY)
soundcloud_client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_KEY)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("PLAYMUZIK_DATABASE_URL",settings.PLAYMUZIK_DATABASE_URL)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

celery = Celery('tasks', broker='amqp://guest@localhost//')

class Muzik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url  = db.Column(db.String(200), unique=True)
    name  = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    url  = db.Column(db.String(200), unique=True)
    beat  = db.Column(db.String(50))
    tempo  = db.Column(db.String(50))
    energy  = db.Column(db.String(50))
    danceability  = db.Column(db.String(50))
    duration  = db.Column(db.String(50))
    loudness  = db.Column(db.String(50))
    key  = db.Column(db.String(50))
    mode  = db.Column(db.String(50))
    time_signature  = db.Column(db.String(50))
    register_date =  db.Column(db.DateTime)

    def __init__(self,name,artist=None,url=None,data=None):
        self.name = name
        self.artist = artist
        self.url = url
#        self.beat = data.beats
        self.tempo = data.tempo
        self.enegy = data.energy
        self.danceability = data.danceability
        self.duration = data.duration
        self.loudness = data.loudness
        self.key = data.key
        self.mode = data.mode
        self.time_signature = data.time_signature
        self.register_date = datetime.utcnow()

    def __repr__(self):
        return '<Muzik %r>' % self.name

    @classmethod
    def save(cls,name,artist,url,data):
        track_data = data.analysis.pyechonest_track
        muzik = Muzik(name,artist,url,track_data)
        db.session.add(muzik)
        db.session.commit()
        return True

    @classmethod
    def get_recent(cls,num=50):
        return Muzik.query.order_by(Muzik.register_date).limit(num).all()

@celery.task
def get_soundcloud_muzik(sound_url):
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

@celery.task
def get_youtube_muzik(url):
    value = ""
    artist = None
    
    filepath = compat_str(settings.YOUTUBE_PATH + generate_filename())
    y = YoutubeDL({"format":"18/34/35/5/17","outtmpl":filepath}) 
    y.add_default_info_extractors()
    y.add_post_processor(FFmpegExtractAudioPP(preferredcodec="mp3"))
    value = y.download([url])

    name = get_youtube_title(url)
    data = analyse_muzik(filepath)
    result = save_to_database(name,artist,url,data)
    return result

def analyse_muzik(filename=None):
    data = LocalAudioFile(filename)
    return data
    
def save_to_database(name,artist,url,data):
    result = Muzik.save(name,artist,url,data)
    return result

def get_youtube_title(url):
    try:
        urlldata = urlparse.urlparse(url)
        query = urlparse.parse_qs(urldata.query)
        video_id = query["v"][0]
        yt_service = gdata.youtube.service.YouTubeService()
        query = gdata.youtube.service.YouTubeVideoQuery()
        query.vq = video_id
        feed = yt_service.YouTubeQuery(query)
        name = feed[0].entry.title
    except:
        name = None
    return name

def generate_filename():
   timestamp = time.time()
   return "".join(str(timestamp).split(".")) + ".mp3"

muzik_getter = {"youtube":get_youtube_muzik,"soundcloud":get_soundcloud_muzik}

@app.route("/",methods=["GET"])
def index():
    muzik_list = list()
    if request.method == "GET":
       muzik_list = Muzik.get_recent()
       return render_template("index.html",muzik_list=muzik_list) #TODO templates/index.html bootstrap

@app.route("/submit",methods=["POST"])
def submit():
    if request.method == "POST":
        muzik_url = request.form["muzik_url"] #TODO submit data
        muzik_type = request.form["muzik_type"]
        mod_name = "get_{muzik_type}_muzik".format(muzik_type=muzik_type)
        getattr("muzik",mod_name.delay)(muzik_url) #TODO jobqueue

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/static/<path:filename>')
def send_foo(filename):
    return send_from_directory('static/', filename)

if __name__ == "__main__":
   manager.run()


#http://shkh.hatenablog.com/entry/2013/01/01/192857
#https://github.com/yuvadm/heroku-periodical