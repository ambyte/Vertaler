# -*- coding: UTF-8 -*-


import wx
import os

from src.controllers.maincontroller import ControllerMain
if os.name=="nt":
    from wx.lib.pubsub import setupv1


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
  