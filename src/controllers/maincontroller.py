# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# Copyright (c) 2011 Sergey Gulyaev <astraway@gmail.com>
#
# This file is part of Vertaler.
#
# Vertaler is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Vertaler is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
# ----------------------------------------------------------------------------

""" Start main frame, processing selected text for translating """

import os
import wx
import sys
import time
from src.modules.settings import options
from wx.lib.pubsub import pub
from src.controllers.mainframecontroller import MainFrameController
from src.controllers.popupcontroller import PopUpController
from src.modules.globalevents.handler_global_event import HandlerGlobalEvents
from src.views import notification

if os.name =="posix":
    from posix import popen
elif os.name =="nt":
    from src.modules.clipboardlib import restore_clipboard, run_clipboard
    from src.modules import getnewversion



class ControllerMain():

    def __init__(self):
        publisher = pub.Publisher()
        self.mainFrame = MainFrameController()
        self.popUpFrame = PopUpController()
        if os.name =="posix": self.mainFrame.view.Show()
        self.mainFrame.view.Hide()
        self.mainFrame.view.Bind( wx.EVT_MENU,self.event_exit, self.mainFrame.view.m_menuItemExit  )
        self.mainFrame.tbicon.Bind(wx.EVT_MENU, self.event_exit, id=wx.ID_EXIT)
        self.globalEvents=HandlerGlobalEvents()

        publisher.subscribe(self.get_clipboard_data, "TranslateText")
        publisher.subscribe(self.hide_frames, "HideFrames")

        if os.name =="nt":
            publisher.subscribe(self.version_result, "VERSION")
            getnewversion.NewVersionThread(False)

    def event_exit( self, event ):
        """
        close application and remove taskbar icon, save options
        """
        self.globalEvents.cancel()
        self.mainFrame.settings.set_global_params()
        self.mainFrame.tbicon.RemoveIcon()
        self.mainFrame.tbicon.Destroy()
        self.mainFrame.view.Destroy()
        sys.exit()

    def hide_frames(self,event):

        # Hide PopUpFrame
        event=event.data
        if self.popUpFrame.view.IsShown():
            popUpFrameSize = self.popUpFrame.view.GetSizeTuple()
            popUpFramePos = self.popUpFrame.view.GetPositionTuple()
            if event.Position[0] > popUpFramePos[0]+popUpFrameSize[0] or popUpFramePos[0]>event.Position[0] or \
                popUpFramePos[1]>event.Position[1] or event.Position[1]> popUpFramePos[1]+popUpFrameSize[1]:
                self.popUpFrame.view.Hide()
                options.isRunTranslate=False

        if options.countClickUp!=2:
            # Hide ResultFrame
            if self.popUpFrame.resultController.view.IsShown():
                if not self.popUpFrame.resultController.view.selectLang:
                    textFrameSize = self.popUpFrame.resultController.view.GetSizeTuple()
                    textFramePos = self.popUpFrame.resultController.view.GetPositionTuple()
                    if event.Position[0] > textFramePos[0]+textFrameSize[0] or textFramePos[0]>event.Position[0] or \
                        textFramePos[1]>event.Position[1] or event.Position[1]> textFramePos[1]+textFrameSize[1]:
                        self.popUpFrame.resultController.view.Hide()
                        options.isRunTranslate=False


    def get_clipboard_data(self,isTranslateNow):
        """
        get selection text use clipboard
        """
        isTranslateNow=isTranslateNow.data
        self.popUpFrame.view.Hide()
        if not isTranslateNow:
            self.popUpFrame.showFrame=False
        options.countClickUp=0
        if os.name=="posix":
            try:
                time.sleep(0.1)
                text = popen('xsel').read()
                options.isRunTranslate=True
                self.popUpFrame.dataText = text
                if self.popUpFrame.dataText!="":
                    if isTranslateNow:
                        options.countClickUp=1
                        self.popUpFrame.translate()
                    else:
                        self.popUpFrame.view.Show()
                    self.dblCtrl=0
            except Exception, ex:
                self.popUpFrame.dataText=ex.message.encode('utf-8')
                self.popUpFrame.view.Show()

        elif os.name =="nt":
            self.globalEvents.hookKeyboard(False)
            run_clipboard(self)
            success = False
            data = wx.TextDataObject()
            try:
                if wx.TheClipboard.Open():
                    success = wx.TheClipboard.GetData(data)
                    wx.TheClipboard.Close()
                    if success:
                        self.popUpFrame.dataText = data.GetText().strip()
                        if self.popUpFrame.dataText!="":
                            options.isRunTranslate=True
                            if isTranslateNow:
                                options.countClickUp=1
                                self.popUpFrame.translate()
                            else:
                                self.popUpFrame.view.Show()
            except Exception, ex:
                self.popUpFrame.dataText=ex.message.encode('utf-8')
                self.popUpFrame.view.Show()
            finally:
                restore_clipboard(self)
                self.globalEvents.hookKeyboard()

    def version_result(self, msg):
        if options.version < msg.data:
            if options.enableNotification or msg.data > options.visitedVersion:
                options.enableNotification=True
                options.visitedVersion=msg.data
                self.pop=notification.NotificationFrame(self.mainFrame.view,msg.data)
                self.pop.Show()
