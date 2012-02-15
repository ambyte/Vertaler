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

""" Listen global events from keyboard and mouse"""

import os
import wx
from src.modules.settings import config

if os.name =="posix":
    from posix import popen
elif os.name =="nt":
    import pyHook as hooklib
from wx.lib.pubsub import pub

class HandlerGlobalEvents():

    def __init__(self):
        self.publisher = pub.Publisher()
        self.hm = hooklib.HookManager()
        self.dblCtrl=0
        self.timeMouseUp=0
        self.isTrue=False
        self.ctrlPressed=False
        if os.name =="nt":
            self.hm.KeyAll = self.global_event
            self.hm.HookKeyboard()
            self.hm.MouseAllButtons = self.global_event
            self.hm.HookMouse()
        elif os.name =="posix":
            self.publisher.subscribe(self.global_event, "EventCall")
            self.hm.start()

    def cancel(self):
        if os.name == "posix":
            self.hm.cancel()
        else:
            self.hookKeyboard(False)

    def hookKeyboard(self,state=True):
        if state:
            self.hm.HookKeyboard()
        else:
            self.hm.UnhookKeyboard()

    def global_event(self,event):
        if os.name=="posix":
            event=event.data
        if event.MessageName == "mouse left down":
            wx.CallAfter(self.on_mouse_down_event, event)
        elif event.MessageName == "mouse left up":
            wx.CallAfter(self.on_mouse_up_event, event)
        elif event.MessageName == "mouse right down":
            wx.CallAfter(self.on_mouse_event_hide, event)
        elif event.MessageName == "mouse middle down":
            wx.CallAfter(self.on_mouse_event_hide, event)
        elif event.MessageName == "key down":
            wx.CallAfter(self.on_key_down, event)
        elif event.MessageName == "key up":
            wx.CallAfter(self.on_key_up, event)
        return True


    def on_key_down(self, event):
        """
        Hit test Control button
        """
        if event.Key=="Control_L" or event.Key=="Control_R" or event.Key=='Lcontrol' or event.Key=='Rcontrol':
            self.ctrlPressed=True
        return True

    def on_key_up(self, event):
        """
        Double press Control button
        """
        if event.Key=="Control_L" or event.Key=="Control_R"  or event.Key=='Lcontrol' or event.Key=='Rcontrol':
            self.ctrlPressed=False
            self.dblCtrl+=1
            if self.dblCtrl==1: self.timeKeyUp = event.Time
            if config.useDblControl and self.dblCtrl==2:
                if 300 > event.Time-self.timeKeyUp:
                    self.dblCtrl=0
                    self.timeKeyUp=0
                    wx.CallAfter(self.publisher.sendMessage,"TranslateText", True)
                else:
                    self.dblCtrl=1
                    self.timeKeyUp = event.Time
        return True

    def on_mouse_down_event(self, event):
        """
        Hide PopUpFrame and ResultFrame on mouse event outside frames
        """
        config.countClickUp+=1
        if event.MessageName!='mouse left down':
            return True

        self.timeMouseDown = event.Time
        return True

    def on_mouse_up_event(self, event):
        """
        processing of double mouse click or mouse selection of words
        """
        if event.MessageName!='mouse left up':
            return True
        wx.CallAfter(self.publisher.sendMessage,"HideFrames", event)
        if not config.enableApp:
            return True
        if config.isRunTranslate:
            return True
        if config.useControl and self.ctrlPressed:
            self.isTrue=True
        elif config.useNothing:
            self.isTrue=True
        if self.isTrue:
            # long down mouse, when select text
            if 300 < event.Time-self.timeMouseDown:
                wx.CallAfter(self.publisher.sendMessage,"TranslateText", False)
                self.timeMouseUp=0

            # double click
            if 350 > event.Time-self.timeMouseUp:
                wx.CallAfter(self.publisher.sendMessage,"TranslateText", False)
                self.timeMouseUp=0
            else:
                self.timeMouseUp=event.Time
            self.isTrue=False
        return True

    def on_mouse_event_hide(self, event):
        """
        Hide PopUpFrame on mouse right down
        """
        wx.CallAfter(self.publisher.sendMessage,"HideFrames", event)
        return True


