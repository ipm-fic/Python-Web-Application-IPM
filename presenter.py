import vista
import modelo
import time
import threading

LOAD = 0.3


class Presenter:
    def __init__(self):
        # Variables
        self.backup_interval = None
        self.backup_on_off = None

        # Initialization
        self.vista = vista.MainWindow()
        self.vista.connect_retry(self.on_retry_clicked)
        self.modelo = modelo.Model()
        self.modelo.add_observer(self)
        self.modelo.get_intervals()

    def on_retry_clicked(self, widget):
        if self.modelo.songs_asked == 0:
            thread = threading.Thread(target=self.interval_petition)
            thread.daemon = True
            thread.start()
        else:
            thread = threading.Thread(target=self.retry_song)
            thread.daemon = True
            thread.start()

    def interval_petition(self):
        self.vista.default_view_caller()
        time.sleep(LOAD)
        self.modelo.get_intervals()

    def on_interval_clicked(self, widget, button_name):
        thread = threading.Thread(target=self.songs_petition, args=(button_name,))
        thread.daemon = True
        thread.start()

    def songs_petition(self, button_name):
        self.vista.start_songs_spinner_caller()
        time.sleep(LOAD)
        on_off = self.vista.switch_status()
        self.modelo.get_songs(button_name, on_off)

    def retry_song(self):
        self.vista.default_view_caller()
        time.sleep(LOAD)
        self.modelo.get_songs(self.backup_interval, self.backup_on_off)

    def update(self):
        if self.modelo.error == 1:
            if self.modelo.songs_asked == 1:
                self.backup_interval = self.modelo.interval
                self.backup_on_off = self.modelo.on_off
                self.vista.stop_songs_spinner_caller()
            self.vista.error_view_caller()
        else:
            if self.modelo.response_list != [] and self.modelo.songs_asked == 0:
                self.vista.create_buttons_caller(self.modelo.response_list, self.on_interval_clicked)
                self.vista.interval_view_caller()
            elif self.modelo.response_list != [] and self.modelo.songs_asked == 1:
                self.vista.stop_songs_spinner_caller()
                self.vista.interval_view_caller()
                self.vista.create_response(self.create_response, self.modelo.interval, self.modelo.on_off,
                                           self.modelo.example, self.modelo.response_list)

    @staticmethod
    def start():
        vista.start()

    @staticmethod
    def create_response(interval, on_off, example, content_list):
        vista.ResponseWindow(interval, on_off, example, content_list)
