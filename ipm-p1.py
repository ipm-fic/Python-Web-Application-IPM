#!/usr/bin/env python3

import gi
import json
import random
import webbrowser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from urllib import request

url_songs = "http://localhost:5000/songs"
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


def create_vbox():
    v_box = Gtk.Box()
    v_box.set_orientation(Gtk.Orientation.VERTICAL)
    return v_box


def create_switch():
    switch = Gtk.Switch()
    switch.set_size_request(45, 25)
    return switch


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
        treeview.append_column(column_title)

        renderer_url = Gtk.CellRendererText()
        column_url = Gtk.TreeViewColumn("Url", renderer_url, text=1)
        treeview.append_column(column_url)

        renderer_fav = Gtk.CellRendererText()
        column_fav = Gtk.TreeViewColumn("Favoritos", renderer_fav, text=2)
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
    def __init__(self):
        # Window
        Gtk.Window.__init__(self, title="Interfaz Musical")
        self.set_size_request(600, 400)

        # Main Container
        container_box = create_vbox()
        container_box.set_valign(Gtk.Align.START)
        container_box.set_border_width(30)

        # Switcher Section
        asc_label = Gtk.Label()
        asc_label.set_markup("<b><span size='x-large'>Intervalo Ascendente</span></b>")
        asc_switch = create_switch()
        asc_switch.set_halign(Gtk.Align.CENTER)
        asc_switch.set_margin_top(20)

        container_box.pack_start(asc_label, True, True, 0)
        container_box.pack_start(asc_switch, True, True, 0)

        # Button Section
        interval_label = Gtk.Label()
        interval_label.set_margin_top(25)
        interval_label.set_markup("<b><span size='x-large'>Intervalos</span></b>")
        interval_label.set_halign(Gtk.Align.START)
        flowbox = Gtk.FlowBox()
        flowbox.set_row_spacing(15)
        flowbox.set_column_spacing(15)
        flowbox.set_margin_top(20)
        flowbox.set_max_children_per_line(4)
        self.create_buttons(flowbox, asc_switch)

        container_box.pack_start(interval_label, True, True, 0)
        container_box.pack_start(flowbox, False, False, 0)

        # Add
        self.add(container_box)

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

    def create_buttons(self, flowbox, switch):
        buttons = ["2m", "2M", "3m", "3M", "4j", "4aum", "5j", "6m", "6M", "7m", "7M", "8a"]

        for button in buttons:
            added_item = Gtk.Button.new_with_label(button)
            added_item.set_size_request(30, 70)
            distance = buttons.index(button) + 1
            added_item.connect("clicked", self.on_button_clicked, button, switch, distance)
            flowbox.add(added_item)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
