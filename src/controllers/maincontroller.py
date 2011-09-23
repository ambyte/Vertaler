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

""" Main Controller
 get selection text use clipboard for os windows"""

import os
import wx
if os.name =="posix":
    from posix import popen
    from src.modules import pyxhook as hooklib
elif os.name =="nt":
    from src.modules.clipboardlib import restore_clipboard, run_clipboard
    from src.modules import getnewversion
    import pyHook as hooklib
    import pythoncom
from wx.lib.pubsub import Publisher as pub
from src.controllers.mainframecontroller import MainFrameController
from src.controllers.popupcontroller import PopUpController
from src.modules import options
from src.views import notification
import sys
import time

class ControllerMain():

    def __init__(self):

        self.mainFrame = MainFrameController()
        self.popUpFrame = PopUpController()
        if os.name =="posix": self.mainFrame.view.Show()
        self.mainFrame.view.Hide()
        self.isTrue=False
        self.timeMouseUp=0
        self.timeControl=0
        self.timeMouseDown=0
        self.dblCtrl=0
        options.isRunTranslate=False
        self.ctrlPressed=False
        self.getClip=True
        self.mainFrame.view.Bind(wx.EVT_CLOSE,self.event_exit)
        self.mainFrame.view.Bind( wx.EVT_MENU,self.event_exit, self.mainFrame.view.m_menuItemExit  )
        self.mainFrame.tbicon.Bind(wx.EVT_MENU, self.event_exit, id=wx.ID_EXIT)
        self.hm = hooklib.HookManager()
        if os.name =="nt":
            pub.subscribe(self.version_result, "VERSION")
            getnewversion.NewVersionThread(False)
            self.hm.KeyDown = self.on_key_down
            self.hm.KeyUp = self.on_key_up
            self.hm.HookKeyboard()
            self.hm.MouseMiddleDown = self.on_mouse_event_hide
            self.hm.MouseRightDown = self.on_mouse_event_hide
            self.hm.MouseLeftDown = self.on_mouse_down_event
            self.hm.MouseLeftUp = self.on_mouse_up_event
            self.hm.HookMouse()
            pythoncom.PumpMessages()
        elif os.name =="posix":
            pub.subscribe(self.on_mouse_down_event, "MouseAllButtonsDown")
            pub.subscribe(self.on_mouse_up_event, "MouseAllButtonsUp")
            pub.subscribe(self.on_key_down, "KeyDown")
            pub.subscribe(self.on_key_up, "KeyUp")
            self.hm.start()

    def event_exit( self, event ):
        """
        close application and remove taskbar icon, save options
        """
        if os.name == "posix":
            self.hm.cancel()
        self.mainFrame.settings.set_global_params()
        self.mainFrame.tbicon.RemoveIcon()
        self.mainFrame.tbicon.Destroy()
        self.mainFrame.view.Destroy()
        sys.exit()

    def on_mouse_event_hide(self, event):
        """
        Hide PopUpFrame on mouse right down
        """
        self.popUpFrame.view.Hide()
        return True

    def on_key_down(self, event):
        """
        Hide PopUpFrame on mouse right down
        """
        if os.name=="posix":
            event=event.data
        if event.Key=="Control_L" or event.Key=="Control_R" or event.Key=='Lcontrol' or event.Key=='Rcontrol':
            self.ctrlPressed=True
        return True

    def on_key_up(self, event):
        """
        Hide PopUpFrame on mouse right down
        """
        if os.name=="posix":
            event=event.data
        if event.Key=="Control_L" or event.Key=="Control_R"  or event.Key=='Lcontrol' or event.Key=='Rcontrol':
            self.ctrlPressed=False
            self.dblCtrl+=1
            if self.dblCtrl==1: self.timeKeyUp = event.Time
            if options.useDblControl and self.dblCtrl==2:
                if 200 > event.Time-self.timeKeyUp:
                    self.dblCtrl=0
                    self.timeKeyUp=0
                    self.get_clipboard_data(True)
                else:
                    self.dblCtrl=1
                    self.timeKeyUp = event.Time
        return True

    def hide_frames(self,event):
        # Hide PopUpFrame

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


    def on_mouse_down_event(self, event):
        """
        Hide PopUpFrame and ResultFrame on mouse event outside frames
        """
        options.countClickUp+=1
        if os.name=="posix":
            event=event.data
        if event.MessageName!='mouse left down':
            return True

        self.timeMouseDown = event.Time
        return True

    def on_mouse_up_event(self, event):
        """
        processing of double mouse click or mouse selection of words
        """
        if os.name=="posix":
            event=event.data
        if event.MessageName!='mouse left up':
            return True
        self.hide_frames(event)
        if not options.enableApp:
            return True
        if options.isRunTranslate:
            return True
        if options.useControl and self.ctrlPressed:
            self.isTrue=True
        elif options.useNothing:
            self.isTrue=True
        if self.isTrue:
            # long down mouse, when select text
            if 300 < event.Time-self.timeMouseDown:
                self.popUpFrame.showFrame=False
                self.timeMouseUp=0
                self.get_clipboard_data(False)

            # double click
            if 300 > event.Time-self.timeMouseUp:
                self.popUpFrame.showFrame=False
                self.timeMouseUp=0
                self.get_clipboard_data(False)
            else:
                self.timeMouseUp=event.Time
            self.isTrue=False
        return True


    def get_clipboard_data(self,isTranslateNow):
        """
        get selection text use clipboard
        """
        options.countClickUp=0
        if os.name=="posix":
            try:
                time.sleep(0.1)
                text = popen('xsel').read()
                options.isRunTranslate=True
#                print "get_clipboard_data"
                self.popUpFrame.dataText = text
                if self.popUpFrame.dataText!="":
                    if isTranslateNow:
                        options.countClickUp=1
                        self.popUpFrame.translate()
                    else:
                        self.popUpFrame.view.Show()
                    self.dblCtrl=0
            except Exception, ex:
                self.popUpFrame.dataText='error: '+sys.exc_info()[0].message.encode('utf-8')
                self.popUpFrame.view.Show()

        elif os.name =="nt":
            self.hm.UnhookKeyboard()
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
#                            self.dblCtrl=0
            except Exception, ex:
                self.popUpFrame.dataText='error: '+sys.exc_info()[0].message.encode('utf-8')
                self.popUpFrame.view.Show()
            finally:
                if os.name =="nt":
                    restore_clipboard(self)
                    self.hm.HookKeyboard()

    def version_result(self, msg):
        if options.version < msg.data:
            if options.enableNotification or msg.data > options.visitedVersion:
                options.enableNotification=True
                options.visitedVersion=msg.data
                self.pop=notification.NotificationFrame(self.mainFrame.view,msg.data)
                self.pop.Show()
