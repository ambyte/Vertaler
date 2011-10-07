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

""" Controller for PopUpFrame """

import webbrowser
import wx
import sys
import os
if os.name =="nt":
    import win32gui
    from src.modules import clipboardlib
elif os.name =="posix":
    from Xlib import display
from wx.lib.pubsub import Publisher as pub
from src.views.popupframe import PopUpFrame
from src.controllers.resultcontroller import ResultController


from src.modules import gettext_windows, options



class PopUpController:

    def __init__(self):
         self.view = PopUpFrame(None)
         self.resultController = ResultController()
         self.dataText=""
         self.showFrame=False

         self.timer = wx.Timer(self.view, wx.ID_ANY)

         # Connect Events

         self.view.Bind( wx.EVT_TIMER, self.on_timer, self.timer )
         self.view.Bind( wx.EVT_KILL_FOCUS, self.on_mouse_event_hide )
         self.view.Bind( wx.EVT_SHOW, self.event_show )
         self.view.Bind( wx.EVT_ENTER_WINDOW, self.event_enter )
         self.view.Bind( wx.EVT_LEAVE_WINDOW, self.event_leave )
         self.view.p_bitmapTranslate.Bind( wx.EVT_LEFT_DOWN, self.event_translate )
         self.view.p_bitmapCopy.Bind( wx.EVT_LEFT_DOWN, self.event_copy )
         self.view.p_bitmapSearch.Bind( wx.EVT_LEFT_DOWN, self.event_search )
         self.view.p_bitmapOpenMain.Bind( wx.EVT_LEFT_DOWN, self.event_open_main )
         self.view.p_bitmapClose.Bind( wx.EVT_LEFT_DOWN, self.event_close )

    def on_mouse_event_hide(self, event):
        """
        Hide frame if kill focus
        """
        self.timer.Stop()
        self.view.Hide()

    def event_show(self, event):
        """
        Event when frame show,
        set position of frame and set timer 3 sec. after that frame hide 
        """
        
        if not self.showFrame:
#            print "popup show"
            self.showFrame=True
            cursorPos=[]
            if os.name =="nt":
                cursorPos=win32gui.GetCursorPos()
            elif os.name =="posix":
                data = display.Display().screen().root.query_pointer()._data
                cursorPos.append(data["root_x"])
                cursorPos.append(data["root_y"])
            displaySize=wx.DisplaySize()
            frameSize = self.view.GetSizeTuple()
            if displaySize[0]<cursorPos[0]+frameSize[0]:
                x=cursorPos[0]-frameSize[0]-5
            else:
                x=cursorPos[0]+10
            if displaySize[1]<cursorPos[1]+frameSize[1]:
                y=cursorPos[1]-frameSize[1]
            else:
                y=cursorPos[1]
            self.view.Move((x,y-10))
            self.timer.Start(3000)
        else:
            if os.name =="nt":
                clipboardlib.event_press_ctrl()
            options.isRunTranslate=False

    def on_timer(self, event):
        """
        Hide frame when timer off
        """
        self.timer.Stop()
        options.isRunTranslate=False
        self.view.Hide()

    def event_enter( self, event ):
        """
        Stop timer if cursor on form
        """
        self.timer.Stop()

    def event_leave( self, event ):
        """
        start timer when cursor leave form
        """
        self.timer.Start(3000)

    def event_translate( self, event ):
        """
        show resultFrame and start translate
        """
        self.translate()
        self.view.Hide()


    def translate(self):
#        print "translate"
        options.countClickUp+=1
        self.resultController.countRunTranslator+=1
        self.resultController.view.SetSize((50,17))
        self.resultController.set_position()
        self.resultController.showResult=False
        self.resultController.selectedText=self.dataText
        self.resultController.view.Show(True)

    def event_copy( self, event ):
        """
        Copy selected text
        """
        if os.name =="posix":
            wx.TheClipboard.UsePrimarySelection(primary=False)
            wx.TheClipboard.Close()
        data = wx.TextDataObject()
        data.SetText(self.dataText)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox(_("Unable to open the clipboard"), _("Error"))
        options.isRunTranslate=False
        self.view.Hide()

    def event_search( self, event ):
        """
        Search selected text on browser
        """
        if options.defaultSearchEngine==0:
            webbrowser.open_new_tab('http://www.google.com/search?q='+self.dataText+
                                    '&sourceid=vertalerproject.org&ie=utf-8&oe=utf-8')
        elif options.defaultSearchEngine==1:
            webbrowser.open_new_tab('http://www.bing.com/search?q='+self.dataText+
                                    '&form=OPRTSD&pc=vertalerproject.org')
        elif options.defaultSearchEngine==2:
            webbrowser.open_new_tab('http://search.yahoo.com/search?p='+self.dataText+
                                    '&ei=UTF-8&fr=vertalerproject.org')
        elif options.defaultSearchEngine==3:
            webbrowser.open_new_tab('http://yandex.ru/yandsearch?text='+self.dataText+
                                    '&from=vertalerproject.org')
        options.isRunTranslate=False
        self.view.Hide()
        
    def event_open_main( self, event ):
        """
        Open MainFrame and send selected text
        """
        pub.sendMessage("GO HOME",self.dataText)
        options.isRunTranslate=False
        self.view.Hide()

    def event_close( self, event ):
        """
        Close frame
        """
        options.isRunTranslate=False
        self.view.Hide()
