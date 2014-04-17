import os
import sys
import time
import shutil
import simplejson
import urlparse
import urllib2
from datetime import datetime

from celery import Celery
from flask import Flask, Response,render_template, request, send_from_directory,make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from collections import OrderedDict

import soundcloud
import pyechonest
from gdata.youtube.service import YouTubeService,YouTubeVideoQuery
from audio import LocalAudioFile
import subprocess
from subprocess import Popen
from youtube_dl import YoutubeDL
from youtube_dl.postprocessor import FFmpegExtractAudioPP
from youtube_dl.utils import compat_str,DateRange

try:
    import settings #TODO settings
except:
    import sample_settings as settings
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

pyechonest.config.ECHO_NEST_API_KEY = os.environ.get("ECHO_NEST_API_KEY",settings.ECHO_NEST_API_KEY)
SOUNDCLOUD_CLIENT_KEY = os.environ.get("SOUNDCLOUD_CLIENT_KEY",settings.SOUNDCLOUD_CLIENT_KEY)
soundcloud_client = soundcloud.Client(client_id=SOUNDCLOUD_CLIENT_KEY)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL",settings.PLAYMUZIK_DATABASE_URL)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

celery = Celery('tasks')
celery.config_from_object('celeryconfig')

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
        self.energy = data.energy
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

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

def date_handler(o):
    if hasattr(o, 'isoformat') and callable(o.isoformat):
        return o.isoformat()
    raise TypeError("Can't serialize %r" % (o,))

def muzik_to_json(muzik):
    muzik_list = list()
    # print "muzik",muzik
    map(lambda x:muzik_list.append(x._asdict()),muzik)
    muzik_json = simplejson.dumps(muzik_list,default=date_handler)
    return muzik_json

@celery.task(name="soundcloud")
def get_soundcloud_muzik(sound_url):
    print "soundcloud",sound_url
    s = soundcloud_client.get("/resolve",url=sound_url)
    if s.downloadable and s.original_format == "mp3":
        url = s.download_url
    else:
        url = s.stream_url

    url += "?client_id=" + SOUNDCLOUD_CLIENT_KEY
    result = urllib2.urlopen(url)
    name = s.title
    artist = s.user.get("username")
    filename = "/tmp/" + generate_filename()
    print "write to filename",filename
    with open(filename,"w") as f: #TODO raw mp3 possible to analyse
        f.write(result.read())
    print "analyse start"
    data = analyse_muzik(filename)
    print "save to database",type(data)
    result = save_to_database(name,artist,sound_url,data)
    print "result",result
    return result

def download_youtube(url,filepath,params=None):
    tmp_filepath = compat_str(filepath)
    print "download to",tmp_filepath
    params = params or settings.youtube_params
    params.update({"outtmpl":tmp_filepath,"daterange":DateRange(None,None)})
    y = YoutubeDL(params) 
     #y = YoutubeDL({"format":"18/34/35/5/17","outtmpl":filepath}) 
     #y.print_debug_header()
    y.add_default_info_extractors()
    y.add_post_processor(FFmpegExtractAudioPP(preferredcodec="m4a",preferredquality=5, nopostoverwrites=False))
    value = y.download([url])
    #cmd = 'youtube-dl {url} --extract-audio --audio-format wav -o {filepath}'.format(url=url,filepath=filepath)
    #print cmd
    #result = subprocess.call(cmd,shell=True)
    #print result
    return True

@celery.task
def get_youtube_muzik(url):
    value = ""
    artist = None

    filename = generate_filename(".mp3")
    filepath = settings.YOUTUBE_PATH + filename
    result = download_youtube(url,filepath)
    if not result:
        return
    name = get_youtube_title(url)
    filepath2 = filepath.split(".")[0] + ".m4a" #TODO for some reasons.
    data = analyse_muzik(filepath2)
    result = save_to_database(name,artist,url,data)
    return result

def analyse_muzik(filename=None):
    data = LocalAudioFile(filename)
    return data
    
def save_to_database(name,artist,url,data):
    result = Muzik.save(name,artist,url,data)
    return result

def get_youtube_title(url):
    
        urldata = urlparse.urlparse(url)
        query = urlparse.parse_qs(urldata.query)
        video_id = query["v"][0]
        yt_service = YouTubeService()
        query = YouTubeVideoQuery()
        query.vq = video_id
        feed = yt_service.YouTubeQuery(query)
        name = feed.entry[0].title.text
        return name

def generate_filename(form=".mp3"):
   timestamp = time.time()
   return "".join(str(timestamp).split(".")) + form

muzik_getter = {"youtube":get_youtube_muzik,"soundcloud":get_soundcloud_muzik}



@app.route("/",methods=["GET"])
def index():
    if request.method == "GET":
       print APP_ROOT + "/templates"
       return make_response(open(APP_ROOT + "/templates/index.html").read()) #TODO templates/index.html bootstrap

@app.route("/submit",methods=["POST","GET"])
def submit():
    print "SUBMIT"
    muzik_url = None
    if request.method == "POST":
        muzik_url = request.form["source"]
        status = celery.current_app.control.inspect().ping()
        if "youtube" in muzik_url:
            if status:
               get_youtube_muzik.delay(muzik_url)
            else:
               get_youtube_muzik(muzik_url)
        elif "soundcloud" in muzik_url:
            if status:
               get_soundcloud_muzik.delay(muzik_url)
            else:
               get_soundcloud_muzik(muzik_url)
        else:
            return Response()
        #get_soundcloud_muzik.delay(muzik_url)
    if request.method == "GET":
        muzik_url = request.args.get("url")
        get_soundcloud_muzik.delay(muzik_url)

        # muzik_type = request.form["muzik_type"] #TODO parse muzik_type
        # mod_name = "get_{muzik_type}_muzik".format(muzik_type=muzik_type)
        # getattr("muzik",mod_name.delay)(muzik_url) #TODO jobqueue
    return Response()

@app.route("/result",methods=["POST","GET"])
def result():
    muzik_list = Muzik.get_recent()
    muzik_json= muzik_to_json(muzik_list)
    return Response(muzik_json)

@app.route('/static/<path:filename>')
def send_foo(filename):
    return send_from_directory('static/', filename)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'),404

if __name__ == "__main__":
   manager.run()
   #app.run(debug=True)

