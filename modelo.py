from sqlite3 import OperationalError
from datetime import date
from os.path import join, expanduser
import os

import Config


DATABASE = join(expanduser('~'), '.ControlOrange\\controlOrange.db')

__author__ = 'David'
import sqlite3


class Modelo:
    @staticmethod
    def initbd():
        if not os.path.exists(DATABASE):
            os.mkdir(join(expanduser('~'), '.ControlOrange'))

        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='control'")
        if c.fetchone() is None:
            try:
                c.execute("CREATE TABLE control (date date, downvolume real, upvolume real)")
                conn.commit()
                c.execute("CREATE TABLE config (limite TEXT NOT NULL DEFAULT 30, "
                          "dia TEXT NOT NULL DEFAULT 8, aviso TEXT NOT NULL DEFAULT 90, "
                          "minimizado INTEGER NOT NULL DEFAULT 1  CHECK(minimizado in (1, 0)),"
                          "inicio INTEGER NOT NULL DEFAULT 1 CHECK(inicio in (1, 0)));")
                conn.commit()
                t = ('30', '8', '90', '1', '1')
                c.execute(" insert into config (limite, dia, aviso, minimizado, inicio) values(?,?,?,?,?)", t)
                conn.commit()
                c.execute("CREATE TABLE totales (total_descargado real, fecha date);")
                conn.commit()
                conn.close()
            except OperationalError:
                pass


    @staticmethod
    def actualizardatos(downvolume, upvolume):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        t = (downvolume, upvolume)
        c.execute(" insert into control (date, downvolume, upvolume) values (datetime('now'),?,?)", t)
        conn.commit()
        conn.close()

    @staticmethod
    def actualizarconfiguracion():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        t = (
            str(Config.limiteDescarga), str(Config.reinicio), str(Config.aviso), str(Config.minimizado),
            str(Config.inicio))
        c.execute(" update config set limite=?, dia=?, aviso=?, minimizado=?, inicio=?", t)
        conn.commit()
        conn.close()

    @staticmethod
    def descargaactual():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(" select total_descargado from totales order by fecha desc")
        cursor = c.fetchone()
        if cursor is not None:
            downvolume = cursor[0]
        else:
            downvolume = 0
        conn.close()
        return downvolume

    @staticmethod
    def insertarreinicio(downvolume):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(" insert into totales (fecha, total_descargado) values (datetime('now'),?)", (downvolume, ))
        conn.commit()
        conn.close()

    @staticmethod
    def checkreinicio():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        month = date.today().month
        year = date.today().year
        mesanyo = str(year) + str(month).zfill(2)
        check = True
        c.execute(" select total_descargado from totales where strftime('%Y%m', fecha) = ?", (mesanyo,))
        cursor = c.fetchone()
        if cursor is not None:
            check = False
        conn.close()
        return check


    @staticmethod
    def cargarconfiguracion():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(" select limite, dia, aviso, minimizado, inicio from config")
        row = c.fetchone()
        Config.limiteDescarga = row[0]
        Config.reinicio = row[1]
        Config.aviso = row[2]
        Config.minimizado = row[3]
        Config.inicio = row[4]

        conn.close()

