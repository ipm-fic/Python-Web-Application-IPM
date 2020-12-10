#!/usr/bin/env python3

import gi
import json
import random
import webbrowser
import threading
import time

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
from urllib import request, error

url_songs = "http://localhost:5000/songs"
url_intervals = "http://localhost:5000/intervals"
notes = ["do", "do♯", "re", "re♯", "mi", "fa", "fa♯", "sol", "sol♯", "la", "la♯", "si"]
LOAD = 0.3


def get_interval_distance(interval):
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
    return switcher.get(interval, "Intervalo Inválido")


def get_songs(window):
    try:
        response = request.urlopen(url_songs + "/" + window.interval + "/" + window.on_off)
        data = response.read()
        jsondata = json.loads(data)
        listdata = jsondata["data"]
        response_list = []

        for i in range(len(listdata)):
            response_list.append(listdata[i])

        time.sleep(LOAD)
        GLib.idle_add(window.songs_response, 1, response_list)
    except error.URLError:
        time.sleep(LOAD)
        GLib.idle_add(window.songs_response, 0, None)


def get_intervals(window):
    try:
        response = request.urlopen(url_intervals)
        data = response.read()
        jsondata = json.loads(data)
        response_list = []

        for interval in jsondata["data"]:
            response_list.append(interval)

        time.sleep(LOAD)
        GLib.idle_add(window.interval_response, 1, response_list)
    except error.URLError:
        time.sleep(LOAD)
        GLib.idle_add(window.interval_response, 0, None)


def create_vbox():
    v_box = Gtk.Box()
    v_box.set_orientation(Gtk.Orientation.VERTICAL)
    return v_box


def create_switch():
    switch = Gtk.Switch()
    switch.set_size_request(45, 25)
    return switch


class ResponseWindow(Gtk.Window):
    def __init__(self, interval, on_off):
        # Vars
        self.interval = interval
        self.on_off = on_off

        # Window
        Gtk.Window.__init__(self, title="Respuesta: " + interval + " " + on_off)
        self.set_size_request(500, 300)

        # Thread
        self.songs_petition()

        # Container
        self.container_box = create_vbox()
        self.container_box.set_valign(Gtk.Align.START)
        self.container_box.set_border_width(30)

        # Header
        self.interval_label = Gtk.Label()
        self.interval_label.set_markup("<b><span size='x-large'>Intervalo: </span></b>" + "<span size='x-large'>" +
                                       interval + " " + on_off + "</span>")
        self.interval_label.set_halign(Gtk.Align.START)
        self.example_label = Gtk.Label()
        self.example = self.create_example(on_off)
        self.example_label.set_markup(
            "<b><span size='x-large'>Ejemplo: </span></b>" + "<span size='x-large'>" + self.example + "</span>")
        self.example_label.set_halign(Gtk.Align.START)
        self.example_label.set_margin_top(10)

        self.container_box.pack_start(self.interval_label, True, True, 0)
        self.container_box.pack_start(self.example_label, True, True, 0)

        # Treeview
        self.liststore = Gtk.ListStore(str, str, str)
        self.fav_filter = self.liststore.filter_new()
        self.fav_filter.set_visible_func(self.fav_filter_func)
        self.treeview = Gtk.TreeView(model=self.fav_filter)
        self.treeview.set_margin_top(30)
        self.current_fav_filter = "NO"

        self.renderer_title = Gtk.CellRendererText()
        self.column_title = Gtk.TreeViewColumn("Título", self.renderer_title, text=0)
        self.column_title.set_resizable(True)
        self.treeview.append_column(self.column_title)

        self.renderer_url = Gtk.CellRendererText()
        self.column_url = Gtk.TreeViewColumn("Url", self.renderer_url, text=1)
        self.column_url.set_resizable(True)
        self.treeview.append_column(self.column_url)

        self.renderer_fav = Gtk.CellRendererText()
        self.column_fav = Gtk.TreeViewColumn("Favoritos", self.renderer_fav, text=2)
        self.column_fav.set_resizable(True)
        self.treeview.append_column(self.column_fav)

        self.treeview.connect("row-activated", self.open_url)

        self.container_box.pack_start(self.treeview, False, False, 0)

        # Fav Switcher Section
        self.fav_box = Gtk.Box(spacing=15)
        self.fav_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.fav_box.set_halign(Gtk.Align.CENTER)
        self.fav_box.set_margin_top(30)
        self.fav_label = Gtk.Label()
        self.fav_label.set_markup("<b><span size='x-large'>Sólo Favoritos</span></b>")
        self.fav_switch = create_switch()
        self.fav_switch.connect("notify::active", self.on_switch_used, self.fav_switch)
        self.fav_switch.set_halign(Gtk.Align.CENTER)

        self.fav_box.pack_start(self.fav_label, True, True, 0)
        self.fav_box.pack_start(self.fav_switch, True, True, 0)

        self.container_box.pack_start(self.fav_box, False, False, 0)

        # Default & Error view
        self.spin = Gtk.Spinner()
        self.spin.set_halign(Gtk.Align.CENTER)
        self.spin.set_size_request(35, 35)
        self.spin.start()

        self.error_h1 = Gtk.Label()
        self.error_h1.set_markup("<b><span size='xx-large'>Error</span></b>")
        self.error_p = Gtk.Label()
        self.error_p.set_markup("No se ha podido conectar con el servidor")
        self.error_button = Gtk.Button.new_with_label(label="Reintentar")
        self.error_button.set_margin_top(20)
        self.error_button.set_size_request(30, 20)
        self.error_button.connect("clicked", self.on_retry_clicked)

        self.container_box.pack_start(self.error_h1, True, True, 0)
        self.container_box.pack_start(self.error_p, True, True, 0)
        self.container_box.pack_start(self.error_button, False, False, 0)
        self.container_box.pack_start(self.spin, True, True, 0)

        # Add
        self.add(self.container_box)

        self.default_view()

    @staticmethod
    def fill_treeview(liststore, interval, on_off, interval_list):

        for i in range(len(interval_list)):
            liststore.append([interval_list[i][0], interval_list[i][1], interval_list[i][2]])

    def fav_filter_func(self, model, iteri, data):
        if self.current_fav_filter == "NO":
            return True
        else:
            return model[iteri][2] == "YES"

    def on_retry_clicked(self, widget):
        self.error_button.hide()
        self.error_h1.hide()
        self.error_p.hide()
        self.spin.start()
        self.songs_petition()

    def on_switch_used(self, widget, gparam, switch):
        if switch.get_active():
            self.current_fav_filter = "YES"
        else:
            self.current_fav_filter = "NO"
        self.fav_filter.refilter()

    def create_example(self, on_off):
        fst_note = notes.index(random.choice(notes))
        distance = get_interval_distance(self.interval)
        if on_off == "asc":
            snd_note = (fst_note + distance) % 12
            return notes[fst_note] + " - " + notes[snd_note]
        else:
            snd_note = (fst_note - distance) % 12
            return notes[fst_note] + " - " + notes[snd_note]

    def default_view(self):
        self.container_box.set_valign(Gtk.Align.CENTER)
        self.container_box.show()
        self.spin.show()

    def songs_petition(self):
        thread = threading.Thread(target=get_songs, args=(self,))
        thread.daemon = True
        thread.start()

    def songs_response(self, control, songs_list):
        self.spin.stop()
        if control == 0:
            self.error_h1.show()
            self.error_p.show()
            self.error_button.show()
        else:
            self.container_box.set_valign(Gtk.Align.START)
            self.interval_label.show()
            self.example_label.show()
            self.fill_treeview(self.liststore, self.interval, self.on_off, songs_list)
            self.treeview.show_all()
            self.fav_box.show_all()

    def open_url(self, view, row, column):
        if self.liststore[row][1] != "":
            webbrowser.open(self.liststore[row][1])


class MainWindow(Gtk.Window):
    def __init__(self):
        # Window
        Gtk.Window.__init__(self, title="Interfaz Musical")
        self.set_size_request(600, 400)

        # Create thread for interval petition
        self.interval_petition()

        # Main Container
        self.container_box = create_vbox()
        self.container_box.set_valign(Gtk.Align.START)
        self.container_box.set_border_width(30)

        # Switcher Section
        self.asc_label = Gtk.Label()
        self.asc_label.set_markup("<b><span size='x-large'>Intervalo Ascendente</span></b>")
        self.asc_switch = create_switch()
        self.asc_switch.set_halign(Gtk.Align.CENTER)
        self.asc_switch.set_margin_top(20)

        self.container_box.pack_start(self.asc_label, True, True, 0)
        self.container_box.pack_start(self.asc_switch, True, True, 0)

        # Button Section
        self.interval_label = Gtk.Label()
        self.interval_label.set_margin_top(25)
        self.interval_label.set_markup("<b><span size='x-large'>Intervalos</span></b>")
        self.interval_label.set_halign(Gtk.Align.START)
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_row_spacing(15)
        self.flowbox.set_column_spacing(15)
        self.flowbox.set_margin_top(20)
        self.flowbox.set_max_children_per_line(4)

        self.container_box.pack_start(self.interval_label, True, True, 0)
        self.container_box.pack_start(self.flowbox, False, False, 0)

        # Default & Error view
        self.spin = Gtk.Spinner()
        self.spin.set_halign(Gtk.Align.CENTER)
        self.spin.set_size_request(35, 35)
        self.spin.start()

        self.error_h1 = Gtk.Label()
        self.error_h1.set_markup("<b><span size='xx-large'>Error</span></b>")
        self.error_p = Gtk.Label()
        self.error_p.set_markup("No se ha podido conectar con el servidor")
        self.error_button = Gtk.Button.new_with_label(label="Reintentar")
        self.error_button.set_margin_top(20)
        self.error_button.set_size_request(30, 20)
        self.error_button.connect("clicked", self.on_retry_clicked)

        self.container_box.pack_start(self.error_h1, True, True, 0)
        self.container_box.pack_start(self.error_p, True, True, 0)
        self.container_box.pack_start(self.error_button, False, False, 0)
        self.container_box.pack_start(self.spin, True, True, 0)

        # Add
        self.add(self.container_box)

        # Load default view
        self.default_view()

    def default_view(self):
        self.container_box.set_valign(Gtk.Align.CENTER)
        self.container_box.show()
        self.spin.show()

    def on_retry_clicked(self, widget):
        self.error_button.hide()
        self.error_h1.hide()
        self.error_p.hide()
        self.spin.start()
        self.interval_petition()

    def interval_petition(self):
        thread = threading.Thread(target=get_intervals, args=(self,))
        thread.daemon = True
        thread.start()

    @staticmethod
    def switch_status(switch):
        if switch.get_active():
            return "asc"
        else:
            return "des"

    @staticmethod
    def create_response(interval, on_off):
        response = ResponseWindow(interval, on_off)
        response.show()

    def call_response(self, interval, switch):
        on_off = self.switch_status(switch)
        GLib.idle_add(self.create_response, interval, on_off)

    def on_button_clicked(self, widget, interval, switch):
        thread = threading.Thread(target=self.call_response, args=(interval, switch))
        thread.daemon = True
        thread.start()

    def create_buttons(self, flowbox, switch, interval_list):

        for button in interval_list:
            added_item = Gtk.Button.new_with_label(button)
            added_item.set_size_request(30, 70)
            added_item.connect("clicked", self.on_button_clicked, button, switch)
            flowbox.add(added_item)

    def interval_response(self, control, interval_list):
        self.spin.stop()
        if control == 0:
            self.error_h1.show()
            self.error_p.show()
            self.error_button.show()
        else:
            self.container_box.set_valign(Gtk.Align.START)
            self.asc_label.show()
            self.asc_switch.show()
            self.interval_label.show()
            self.create_buttons(self.flowbox, self.asc_switch, interval_list)
            self.flowbox.show_all()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show()
Gtk.main()
