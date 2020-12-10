import gi
import webbrowser

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib


class MainWindow(Gtk.Window):
    def __init__(self):

        # Window
        self.w = Gtk.Window(title="Interfaz Musical")
        self.w.set_size_request(600, 400)
        self.w.connect("destroy", Gtk.main_quit)

        # Container
        self.container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.container_box.set_valign(Gtk.Align.START)
        self.container_box.set_border_width(30)

        # Switcher Section
        self.asc_label = Gtk.Label()
        self.asc_label.set_markup("<b><span size='x-large'>Intervalo Ascendente</span></b>")
        self.asc_switch = Gtk.Switch()
        self.asc_switch.set_halign(Gtk.Align.CENTER)
        self.asc_switch.set_margin_top(20)

        self.container_box.pack_start(self.asc_label, False, False, 0)
        self.container_box.pack_start(self.asc_switch, False, False, 0)

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

        self.container_box.pack_start(self.interval_label, False, False, 0)
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
        self.hbox_button = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.hbox_button.set_halign(Gtk.Align.CENTER)
        self.hbox_button.set_valign(Gtk.Align.CENTER)
        self.error_button = Gtk.Button.new_with_label(label="Reintentar")
        self.error_button.set_margin_top(20)
        self.error_button.set_size_request(30, 20)
        self.hbox_button.pack_start(self.error_button, False, False, 0)

        self.container_box.pack_start(self.error_h1, False, False, 0)
        self.container_box.pack_start(self.error_p, False, False, 0)
        self.container_box.pack_start(self.hbox_button, False, False, 0)
        self.container_box.pack_start(self.spin, False, False, 0)

        # Spinner for loading a selected interval
        self.songs_spinner = Gtk.Spinner()
        self.songs_spinner.set_size_request(35, 35)
        self.songs_spinner.set_halign(Gtk.Align.CENTER)
        self.songs_spinner.set_margin_top(25)

        self.container_box.pack_start(self.songs_spinner, False, False, 0)

        self.w.add(self.container_box)

        self.w.show()
        self.container_box.show()
        self.default_view()

    def default_view(self):
        self.hide_error()
        self.hide_intervals()
        self.show_default()

    def interval_view(self):
        self.hide_default()
        self.hide_error()
        self.show_intervals()

    def error_view(self):
        self.hide_default()
        self.hide_intervals()
        self.show_error()

    def show_default(self):
        self.container_box.set_valign(Gtk.Align.CENTER)
        self.spin.start()
        self.spin.show()

    def show_error(self):
        self.container_box.set_valign(Gtk.Align.CENTER)
        self.error_h1.show()
        self.error_p.show()
        self.hbox_button.show_all()

    def show_intervals(self):
        self.container_box.set_valign(Gtk.Align.START)
        self.asc_label.show()
        self.asc_switch.show()
        self.interval_label.show()
        self.flowbox.show_all()

    def hide_default(self):
        self.spin.stop()
        self.spin.hide()

    def hide_intervals(self):
        self.asc_label.hide()
        self.asc_switch.hide()
        self.flowbox.hide()
        self.interval_label.hide()
        self.songs_spinner_stop()

    def hide_error(self):
        self.error_h1.hide()
        self.error_p.hide()
        self.hbox_button.hide()

    def songs_spinner_start(self):
        self.songs_spinner.start()
        self.songs_spinner.show()

    def songs_spinner_stop(self):
        self.songs_spinner.stop()
        self.songs_spinner.hide()

    def create_buttons(self, interval_list, handler):
        if self.flowbox.get_child_at_index(0) is not None:
            pass
        else:
            for button in interval_list:
                added_item = Gtk.Button.new_with_label(button)
                added_item.set_size_request(30, 70)
                added_item.connect("clicked", handler, button)
                self.flowbox.add(added_item)

    def connect_retry(self, handler):
        self.error_button.connect("clicked", handler)

    def switch_status(self):
        if self.asc_switch.get_active():
            return "asc"
        else:
            return "des"

    @staticmethod
    def create_response(handler, interval, on_off, example, content_list):
        GLib.idle_add(handler, interval, on_off, example, content_list)

    def error_view_caller(self):
        GLib.idle_add(self.error_view)

    def interval_view_caller(self):
        GLib.idle_add(self.interval_view)

    def create_buttons_caller(self, interval_list, handler):
        GLib.idle_add(self.create_buttons, interval_list, handler)

    def stop_songs_spinner_caller(self):
        GLib.idle_add(self.songs_spinner.stop)

    def start_songs_spinner_caller(self):
        GLib.idle_add(self.songs_spinner_start)

    def default_view_caller(self):
        GLib.idle_add(self.default_view)


class ResponseWindow(Gtk.Window):
    def __init__(self, interval, on_off, example, content_list):

        # Variables
        self.interval = interval
        self.on_off = on_off
        self.example = example
        self.content_list = content_list

        # Window
        self.w = Gtk.Window(title="Respuesta: " + self.interval + " " + self.on_off)
        self.w.set_size_request(500, 300)

        # Container
        self.container_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.container_box.set_valign(Gtk.Align.START)
        self.container_box.set_border_width(30)

        # Header
        self.interval_label = Gtk.Label()
        self.interval_label.set_markup("<b><span size='x-large'>Intervalo: </span></b>" + "<span size='x-large'>" +
                                       self.interval + " " + self.on_off + "</span>")
        self.interval_label.set_halign(Gtk.Align.START)
        self.example_label = Gtk.Label()
        self.example_label.set_markup(
            "<b><span size='x-large'>Ejemplo: </span></b>" + "<span size='x-large'>" + self.example + "</span>")
        self.example_label.set_halign(Gtk.Align.START)
        self.example_label.set_margin_top(10)

        self.container_box.pack_start(self.interval_label, False, False, 0)
        self.container_box.pack_start(self.example_label, False, False, 0)

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

        self.fill_treeview()
        self.treeview.connect("row-activated", self.open_url)

        self.container_box.pack_start(self.treeview, False, False, 0)

        # Fav Switcher Section
        self.fav_box = Gtk.Box(spacing=15)
        self.fav_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.fav_box.set_halign(Gtk.Align.CENTER)
        self.fav_box.set_margin_top(30)
        self.fav_label = Gtk.Label()
        self.fav_label.set_markup("<b><span size='x-large'>Sólo Favoritos</span></b>")
        self.fav_switch = Gtk.Switch()
        self.fav_switch.set_size_request(45, 25)
        self.fav_switch.connect("notify::active", self.on_switch_used)
        self.fav_switch.set_halign(Gtk.Align.CENTER)

        self.fav_box.pack_start(self.fav_label, False, False, 0)
        self.fav_box.pack_start(self.fav_switch, False, False, 0)

        self.container_box.pack_start(self.fav_box, False, False, 0)

        self.w.add(self.container_box)
        self.w.show_all()


    def fav_filter_func(self, model, iteri, data):
        if self.current_fav_filter == "NO":
            return True
        else:
            return model[iteri][2] == "YES"

    def fill_treeview(self):
        for i in range(len(self.content_list)):
            self.liststore.append([self.content_list[i][0], self.content_list[i][1], self.content_list[i][2]])

    def on_switch_used(self, widget, gparam):
        if self.fav_switch.get_active():
            self.current_fav_filter = "YES"
        else:
            self.current_fav_filter = "NO"
        self.fav_filter.refilter()

    def open_url(self, view, row, column):
        if self.liststore[row][1] != "":
            webbrowser.open(self.liststore[row][1])


def start():
    Gtk.main()
