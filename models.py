#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

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

    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result

def save_to_database(name,artist,url,data):
    result = Muzik.save(name,artist,url,data)
    return result