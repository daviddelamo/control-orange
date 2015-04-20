from datetime import date

from modelo import Modelo
import Config


__author__ = 'David'

import threading
import urllib2


class ThreadControl(threading.Thread):
    global modelo
    global icon

    def __init__(self, icon):
        self.modelo = Modelo()
        self.icon = icon
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
        while not self.event.is_set():
            page = urllib2.urlopen("http://192.168.1.1/html/status/waninforefresh.asp")
            html = page.read()
            words = html.split('\'')
            upvolume = 0
            downvolume = 0
            downrate = 0
            uprate = 0
            counter = 0
            for word in words:
                if counter == 3:
                    uprate = float(word)
                elif counter == 7:
                    downrate = float(word)
                elif counter == 11:
                    upvolume = float(word)
                elif counter == 15:
                    downvolume = float(word)
                counter += 1

            descarga_actual = self.modelo.descargaactual()

            self.modelo.actualizardatos((downvolume - descarga_actual), upvolume)
            self.icon.actualizaballoon((downvolume - descarga_actual))
            day = date.today().day

            if str(day) >= str(Config.reinicio):
                if self.modelo.checkreinicio():
                    self.modelo.insertarreinicio(downvolume)

            self.event.wait(30)