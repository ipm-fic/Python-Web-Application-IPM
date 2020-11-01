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


def get_songs(interval, asc_des):
    response = request.urlopen(url_songs + "/" + interval + "/" + asc_des)
    data = response.read()
    jsondata = json.loads(data)
    listdata = jsondata["data"]
    response_list = []

    for i in range(len(listdata)):
        response_list.append(listdata[i])

    return response_list


def get_intervals(main_window):
    try:
        response = request.urlopen(url_intervals)
        data = response.read()
        jsondata = json.loads(data)
        response_list = []

        for interval in jsondata["data"]:
            response_list.append(interval)

        time.sleep(0.5)
        GLib.idle_add(main_window.update_view, response_list, 1)
    except error.URLError:
        time.sleep(0.5)
        GLib.idle_add(main_window.update_view, "Error", 0)


def create_vbox():
    v_box = Gtk.Box()
    v_box.set_orientation(Gtk.Orientation.VERTICAL)
    return v_box


def create_switch():
    switch = Gtk.Switch()
    switch.set_size_request(45, 25)
    return switch


class Controller:
    def __init__(self):
        self.main_window = MainWindow(self)
        self.main_window.default_view()
        self.interval_petition()

    def execute(self):
        Gtk.main()

    def interval_petition(self):
        thread = threading.Thread(target=get_intervals, args=(self.main_window,))
        thread.daemon = True
        thread.start()

    def on_retry_clicked(self, widget):
        self.main_window.spin.start()
        self.main_window.error_btn.hide()
        self.main_window.error_h1.hide()
        self.main_window.error_sub_h1.hide()
        self.interval_petition()


class ResponseWindow(Gtk.Window):
    def __init__(self, interval, on_off, distance):
        # Window
        Gtk.Window.__init__(self, title="Respuesta: " + interval + " " + on_off)
        self.set_size_request(500, 300)

        # Container
        container_box = create_vbox()
        container_box.set_valign(Gtk.Align.START)
        container_box.set_border_width(30)

        # Header
        interval_label = Gtk.Label()
        interval_label.set_markup("<b><span size='x-large'>Intervalo: </span></b>" + "<span size='x-large'>" +
                                  interval + " " + on_off + "</span>")
        interval_label.set_halign(Gtk.Align.START)
        example_label = Gtk.Label()
        example = self.create_example(distance, on_off)
        example_label.set_markup(
            "<b><span size='x-large'>Ejemplo: </span></b>" + "<span size='x-large'>" + example + "</span>")
        example_label.set_halign(Gtk.Align.START)
        example_label.set_margin_top(10)

        container_box.pack_start(interval_label, True, True, 0)
        container_box.pack_start(example_label, True, True, 0)

        # Treeview
        self.liststore = Gtk.ListStore(str, str, str)
        self.fav_filter = self.liststore.filter_new()
        self.fav_filter.set_visible_func(self.fav_filter_func)
        treeview = Gtk.TreeView(model=self.fav_filter)
        treeview.set_margin_top(30)
        self.current_fav_filter = "NO"

        renderer_title = Gtk.CellRendererText()
        column_title = Gtk.TreeViewColumn("Título", renderer_title, text=0)
        column_title.set_resizable(True)
        treeview.append_column(column_title)

        renderer_url = Gtk.CellRendererText()
        column_url = Gtk.TreeViewColumn("Url", renderer_url, text=1)
        column_url.set_resizable(True)
        treeview.append_column(column_url)

        renderer_fav = Gtk.CellRendererText()
        column_fav = Gtk.TreeViewColumn("Favoritos", renderer_fav, text=2)
        column_fav.set_resizable(True)
        treeview.append_column(column_fav)

        treeview.connect("row-activated", self.open_url)

        container_box.pack_start(treeview, False, False, 0)

        # Fav Switcher Section
        fav_box = Gtk.Box(spacing=15)
        fav_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        fav_box.set_halign(Gtk.Align.CENTER)
        fav_box.set_margin_top(30)
        fav_label = Gtk.Label()
        fav_label.set_markup("<b><span size='x-large'>Sólo Favoritos</span></b>")
        fav_switch = create_switch()
        fav_switch.connect("notify::active", self.on_switch_used, fav_switch)
        fav_switch.set_halign(Gtk.Align.CENTER)

        fav_box.pack_start(fav_label, True, True, 0)
        fav_box.pack_start(fav_switch, True, True, 0)

        container_box.pack_start(fav_box, False, False, 0)

        # Add
        self.fill_treeview(self.liststore, interval, on_off)
        self.add(container_box)

    @staticmethod
    def fill_treeview(liststore, interval, on_off):
        interval_list = get_songs(interval, on_off)
        for i in range(len(interval_list)):
            liststore.append([interval_list[i][0], interval_list[i][1], interval_list[i][2]])

    def fav_filter_func(self, model, iteri, data):
        if self.current_fav_filter == "NO":
            return True
        else:
            return model[iteri][2] == "YES"

    def on_switch_used(self, widget, gparam, switch):
        if switch.get_active():
            self.current_fav_filter = "YES"
        else:
            self.current_fav_filter = "NO"
        self.fav_filter.refilter()

    @staticmethod
    def create_example(distance, on_off):
        fst_note = notes.index(random.choice(notes))
        if on_off == "asc":
            snd_note = (fst_note + distance) % 12
            return notes[fst_note] + " - " + notes[snd_note]
        else:
            snd_note = (fst_note - distance) % 12
            return notes[fst_note] + " - " + notes[snd_note]

    def open_url(self, view, row, column):
        if self.liststore[row][1] != "":
            webbrowser.open(self.liststore[row][1])


class MainWindow(Gtk.Window):
    def __init__(self, control):
        # Window
        self.win = Gtk.Window(title="Interfaz Musical")
        self.win.set_size_request(600, 400)

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

        # Error
        self.error_h1 = Gtk.Label()
        self.error_h1.set_halign(Gtk.Align.CENTER)
        self.error_h1.set_markup("<b><span size='xx-large'>Error</span></b>")
        self.error_sub_h1 = Gtk.Label()
        self.error_sub_h1.set_halign(Gtk.Align.CENTER)
        self.error_sub_h1.set_markup("No se pudo conectar al servidor")
        self.error_btn = Gtk.Button.new_with_label(label="Reintentar Conexion")
        self.error_btn.set_margin_top(20)
        self.error_btn.connect("clicked", control.on_retry_clicked)
        self.spin = Gtk.Spinner()
        self.spin.set_size_request(35, 35)
        self.container_box.pack_start(self.error_h1, True, True, 0)
        self.container_box.pack_start(self.error_sub_h1, True, True, 0)
        self.container_box.pack_start(self.error_btn, True, True, 0)
        self.container_box.pack_start(self.spin, True, True, 0)

        # Add
        self.win.add(self.container_box)
        self.win.connect("destroy", Gtk.main_quit)
        self.win.show()

    @staticmethod
    def switch_status(switch):
        if switch.get_active():
            return "asc"
        else:
            return "des"

    def on_button_clicked(self, widget, interval, switch, distance):
        on_off = self.switch_status(switch)
        response = ResponseWindow(interval, on_off, distance)
        response.show_all()

    def create_buttons(self, flowbox, switch, interval_list):

        for button in interval_list:
            added_item = Gtk.Button.new_with_label(button)
            added_item.set_size_request(30, 70)
            distance = interval_list.index(button) + 1
            added_item.show()
            added_item.connect("clicked", self.on_button_clicked, button, switch, distance)
            flowbox.add(added_item)

    def default_view(self):
        self.container_box.show()
        self.container_box.set_valign(Gtk.Align.CENTER)
        self.spin.set_halign(Gtk.Align.CENTER)
        self.spin.set_valign(Gtk.Align.CENTER)
        self.spin.set_size_request(35, 35)
        self.spin.show()
        self.spin.start()

    def update_view(self, interval_list, value):
        self.spin.stop()
        if value == 0:
            self.error_btn.show()
            self.error_h1.show()
            self.error_sub_h1.show()
        else:
            self.asc_label.show()
            self.asc_switch.show()
            self.interval_label.show()
            self.flowbox.show()
            self.create_buttons(self.flowbox, self.asc_switch, interval_list)


build = Controller()
build.execute()
