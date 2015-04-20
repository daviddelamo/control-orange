__author__ = 'David'

import os

from modelo import Modelo
import wx
import Config
import _winreg


RUTA_REGISTRO = 'Software\Microsoft\Windows\CurrentVersion\Run'


class ConfigureDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(ConfigureDialog, self).__init__(*args, **kw)
        self.SetSize((250, 200))
        self.SetTitle("Configurar ControlOrange")
        pnlLimites = wx.Panel(self)
        pnlInicio = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hboxConfiguraciones = wx.BoxSizer(wx.HORIZONTAL)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        sbLimites = wx.StaticBox(pnlLimites, label='Limites')
        sbsLimites = wx.StaticBoxSizer(sbLimites, orient=wx.VERTICAL)

        self.txtLimite = wx.TextCtrl(pnlLimites)
        self.txtLimite.SetValue(Config.limiteDescarga)
        self.txtLimite.SetHelpText("Limite de la tarifa en Gb")
        self.txtReinicio = wx.TextCtrl(pnlLimites)
        self.txtReinicio.SetValue(Config.reinicio)
        self.txtReinicio.SetHelpText("Dia de facturacion o reinicio de la tarifa plana")
        self.txtAviso = wx.TextCtrl(pnlLimites)
        self.txtAviso.SetValue(Config.aviso)
        self.txtAviso.SetHelpText("Porcentaje del consumo a partir del cual se avisara de gasto excesivo.")

        sbsLimites.Add(wx.StaticText(pnlLimites, label='Limite de descarga:'))
        sbsLimites.Add(self.txtLimite)
        sbsLimites.Add(wx.StaticText(pnlLimites, label='Dia de reinicio:'))
        sbsLimites.Add(self.txtReinicio)
        sbsLimites.Add(wx.StaticText(pnlLimites, label='Limite de aviso (Porcentaje del 1 al 99):'))
        sbsLimites.Add(self.txtAviso)

        sbInicio = wx.StaticBox(pnlInicio, label='Configuracion arranque')
        sbsInicio = wx.StaticBoxSizer(sbInicio, orient=wx.VERTICAL)
        self.check_inicio = wx.CheckBox(pnlInicio, label='Iniciar al arrancar el ordenador', style=wx.RB_GROUP)
        if Config.inicio == 1:
            self.check_inicio.Set3StateValue(True)
        sbsInicio.Add(self.check_inicio)
        self.check_minimizado = wx.CheckBox(pnlInicio, label='Iniciar minimizado', style=wx.RB_GROUP)
        if Config.minimizado == 1:
            self.check_minimizado.Set3StateValue(True)
        sbsInicio.Add(self.check_minimizado)

        pnlLimites.SetSizer(sbsLimites)
        pnlInicio.SetSizer(sbsInicio)

        hboxConfiguraciones.Add(pnlLimites, proportion=1,
                                flag=wx.ALIGN_LEFT, border=5)
        hboxConfiguraciones.Add(pnlInicio, proportion=1,
                                flag=wx.ALIGN_RIGHT, border=5)

        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(hboxConfiguraciones, proportion=1,
                 flag=wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox2,
                 flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        self.SetSizer(vbox)
        self.SetSize((500, 300))

        okButton.Bind(wx.EVT_BUTTON, self.OkClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, e):
        self.Destroy()

    def validate(self):
        valid = True
        try:
            reinicio = float(self.txtReinicio.GetLineText(0))
            if reinicio < 1 or reinicio > 31:
                wx.MessageBox('El valor de reinicio debe estar entre 1 y 31', 'Error',
                              wx.OK | wx.ICON_ERROR)
                valid = False
        except ValueError:
            wx.MessageBox('El valor de reinicio debe ser numerico', 'Error',
                          wx.OK | wx.ICON_ERROR)
            valid = False

        try:
            limite = float(self.txtLimite.GetLineText(0))
            if limite < 1:
                wx.MessageBox('El valor de limite debe ser como minimo 1', 'Error',
                              wx.OK | wx.ICON_ERROR)
                valid = False
        except ValueError:
            wx.MessageBox('El valor de limite debe ser numerico', 'Error',
                          wx.OK | wx.ICON_ERROR)
            valid = False

        try:
            aviso = float(self.txtAviso.GetLineText(0))
            if aviso < 1 or aviso > 99:
                wx.MessageBox('El valor de aviso debe estar entre 1 y 99', 'Error',
                              wx.OK | wx.ICON_ERROR)
                valid = False
        except ValueError:
            wx.MessageBox('El valor de aviso debe ser numerico', 'Error',
                          wx.OK | wx.ICON_ERROR)
            valid = False
        return valid

    def OkClose(self, e):

        if self.validate():
            Config.reinicio = self.txtReinicio.GetLineText(0)
            Config.limiteDescarga = self.txtLimite.GetLineText(0)
            Config.aviso = self.txtAviso.GetLineText(0)
            if self.check_inicio.Get3StateValue():
                Config.inicio = 1
                self.inserta_registro_inicio()
            else:
                Config.inicio = 0
                self.borra_registro_inicio()

            if self.check_minimizado.Get3StateValue():
                Config.minimizado = 1
            else:
                Config.minimizado = 0

            Modelo.actualizarconfiguracion()
            self.Destroy()

    def inserta_registro_inicio(self):
        ruta_ejecutable = os.path.dirname(os.path.realpath(__file__)) + '\\ControlOrange.exe'
        keyVal = RUTA_REGISTRO
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal, 0, _winreg.KEY_ALL_ACCESS)
        except:
            key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal)
        _winreg.SetValueEx(key, "ControlOrange", 0, _winreg.REG_SZ, ruta_ejecutable)
        _winreg.CloseKey(key)

    def borra_registro_inicio(self):
        keyVal = RUTA_REGISTRO
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, keyVal, 0, _winreg.KEY_ALL_ACCESS)
        except:
            key = _winreg.CreateKey(_winreg.HKEY_LOCAL_MACHINE, keyVal)

        _winreg.DeleteKey(key, "ControlOrange")
