# -*- coding: UTF-8 -*-


import wx


from src.controllers.maincontroller import ControllerMain
from wx.lib.pubsub import setuparg1


class MainApp(wx.App):
    """
    Start application
    """
    def OnInit(self):
        self.mainController = ControllerMain()
        return True

if __name__ == '__main__':
    app = MainApp(0)
    app.MainLoop()
  