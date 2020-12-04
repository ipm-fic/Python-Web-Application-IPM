# -*- coding: utf-8 -*-

import json
import random
import gettext

from urllib import request, error

_ = gettext.gettext

url_songs = "http://localhost:5000/songs"
url_intervals = "http://localhost:5000/intervals"
notes = [_("do"), _("do♯"), _("re"), _("re♯"), _("mi"), _("fa"), _("fa♯"), _("sol"), _("sol♯"), _("la"), _("la♯"),
         _("si")]


class Model:
    def __init__(self):
        self.response_list = []
        self.songs_asked = None
        self.error = None
        self.observers = set()
        self.interval = None
        self.on_off = None
        self.example = None

    def add_observer(self, observer):
        self.observers.add(observer)

    def notify(self):
        for observer in self.observers:
            observer.update()

    def get_intervals(self):
        try:
            response = request.urlopen(url_intervals)
            data = response.read()
            jsondata = json.loads(data)
            response_list = []

            for interval in jsondata["data"]:
                response_list.append(interval)

            self.response_list = response_list
            self.error = 0
            self.songs_asked = 0
            self.notify()
        except error.URLError:
            self.error = 1
            self.songs_asked = 0
            self.response_list = []
            self.notify()

    def get_songs(self, interval, on_off):
        self.interval = interval
        self.on_off = on_off
        try:
            response = request.urlopen(url_songs + "/" + self.interval + "/" + self.on_off)
            data = response.read()
            jsondata = json.loads(data)
            listdata = jsondata["data"]
            response_list = []

            for i in range(len(listdata)):
                response_list.append(listdata[i])

            self.response_list = response_list
            self.error = 0
            self.songs_asked = 1
            self.example = self.create_example(self.interval, self.on_off)
            self.notify()
        except error.URLError:
            self.error = 1
            self.songs_asked = 1
            self.response_list = []
            self.notify()

    def get_interval_distance(self, interval):
        switcher = {
            "2m": 1,
            "2M": 2,
            "3m": 3,
            "3M": 4,
            "4j": 5,
            "4aum": 6,
            "5j": 7,
            "6m": 8,
            "6M": 9,
            "7m": 10,
            "7M": 11,
            "8a": 12
        }
        invalid_interval = _("Intervalo Invalido")
        return switcher.get(interval, invalid_interval)

    def create_example(self, interval, on_off):
        fst_note = notes.index(random.choice(notes))
        distance = self.get_interval_distance(interval)
        if on_off == "asc":
            snd_note = (fst_note + distance) % 12
            return _(notes[fst_note]) + " - " + _(notes[snd_note])
        else:
            snd_note = (fst_note - distance) % 12
            return _(notes[fst_note]) + " - " + _(notes[snd_note])
