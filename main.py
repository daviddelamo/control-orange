from configure import ConfigureDialog
from threadControl import ThreadControl
from modelo import Modelo
import Config

__author__ = 'David'

import wx

import ctypes

controlOrange = u'dama.org.controlOrange.001'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(controlOrange)

class CustomTaskBarIcon(wx.TaskBarIcon):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, frame):
        """Constructor"""
        wx.TaskBarIcon.__init__(self)
        self.frame = frame

        img = wx.Image("network.png", wx.BITMAP_TYPE_ANY)
        bmp = wx.BitmapFromImage(img)
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(bmp)

        self.SetIcon(self.icon, "Restore")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    def OnTaskBarActivate(self, evt):
        """"""
        pass

    def OnTaskBarClose(self, evt):
        """
        Destroy the taskbar icon and frame from the taskbar icon itself
        """
        self.frame.Close()

    def OnTaskBarLeftClick(self, evt):
        """
        Create the right-click menu
        """
        self.frame.Show()
        self.frame.Restore()

    def CreatePopupMenu(self):
        self.menu = wx.Menu()
        configurar = self.menu.Append(wx.NewId(), "Configurar")
        salir = self.menu.Append(wx.NewId(), "Salir")

        self.Bind(wx.EVT_MENU, self.OnClose, salir)
        self.Bind(wx.EVT_MENU, self.configure, configurar)

        return self.menu

    def actualizaballoon(self, download):
        gbdownload = download / 1024 / 1024 / 1024
        self.SetIcon(self.icon, "Total descargado: " + str("%.2f" % gbdownload) + "Gb")
        # self.ShowBalloon("Total descargado", str("%.2f" % gbdownload) + "Gb")


class MainFrame(wx.Frame):
    """"""

    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Control de ancho de banda")
        panel = wx.Panel(self)
        self.tbIcon = CustomTaskBarIcon(self)
        img = wx.Image("network.png", wx.BITMAP_TYPE_ANY)
        bmp = wx.BitmapFromImage(img)
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(bmp)
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.thread_control = ThreadControl(self.tbIcon)
        self.thread_control.start()
        self.Center()

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        configitem = fileMenu.Append(wx.ID_ANY, 'Configurar', 'Configurar')
        fitem = fileMenu.Append(wx.ID_EXIT, 'Salir', 'Cerrar aplicacion')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.onClose, fitem)
        self.Bind(wx.EVT_MENU, self.configure, configitem)

        if Config.minimizado == 1:
            self.Hide()
        else:
            self.Show()

    def onClose(self, evt):

        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.thread_control.event.set()
        self.Destroy()

    def onMinimize(self, event):
        self.Hide()

    def configure(self, e):
        config = ConfigureDialog(None,
                                 title='Configuracion')
        config.ShowModal()
        config.Destroy()


def main():
    Modelo.initbd()
    Modelo.cargarconfiguracion()
    app = wx.App(False)
    MainFrame()
    app.MainLoop()


if __name__ == "__main__":
    main()