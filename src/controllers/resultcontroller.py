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

""" Controller for ResultFrame """
import os
import time
import wx
from src.views.resultframe import ResultFrame
from src.modules  import translatethread
from src.modules.options import langForTran
from src.modules import options
if os.name =="nt":
    import win32gui
elif os.name =="posix":
    from Xlib import display
from wx.lib.pubsub import Publisher as pub
from src.modules import gettext_windows


class ResultController:

    def __init__(self):
         self.view = ResultFrame(None)
         self.showResult=False
         self.view.ag.Show(True)
         self.countRunTranslator=0
         self.selectedText=""
         self.translatedText=""

         # Connect Events

         self.view.t_choiceLangTo.Bind( wx.EVT_CHOICE, self.event_choice_lang_to )
         self.view.t_choiceLangFrom.Bind( wx.EVT_CHOICE, self.event_choice_lang_from )
         self.view.t_choiceLangTo.Bind( wx.EVT_SET_FOCUS, self.event_select_lang )
         self.view.t_choiceLangFrom.Bind( wx.EVT_SET_FOCUS, self.event_select_lang )
         self.view.t_choiceLangTo.Bind( wx.EVT_KILL_FOCUS, self.event_deselect_lang )
         self.view.t_choiceLangFrom.Bind( wx.EVT_KILL_FOCUS, self.event_deselect_lang )

         self.view.t_bitmapCopy.Bind( wx.EVT_LEFT_DOWN, self.event_copy )
         self.view.m_bitmapClose.Bind( wx.EVT_LEFT_DOWN, self.event_close )
         self.view.Bind( wx.EVT_SHOW, self.event_show )
         self.view.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
         self.view.Bind(wx.EVT_MOTION, self.event_motion)
         pub.subscribe(self.update_display, "TRANSLATE")

    def event_show(self, event):
        """
        Show this frame and start translate text
        """
        if not self.showResult:
            self.hide_controls()
            self.view.Layout()
            self.set_languages()
            self.view.SetFocus()
            self.showResult=True
#            print "show resultframe"
            self.start_translate(options.defaultLangFrom,options.defaultLangTo)
        else:
            options.isRunTranslate=False

    def start_translate(self,langFrom,langTo):
        """
        search languages modules and start translate
        """
        _targetLang=''
        _sourceLang=''
        for k, v in langForTran.iteritems():
            if v==langTo:
                _targetLang=k
            if v==langFrom:
                _sourceLang=k
        if langFrom=='Auto':
            _sourceLang="auto"
#        print "start translate"
        translatethread.TranslateThread(self.selectedText,sourceLang=_sourceLang,targetLang=_targetLang,
                                        countRunTranslator=self.countRunTranslator)

    def set_languages(self):
        """
        set languages name in t_choiceLangFrom and t_choiceLangTo when frame show
        """
        self.languagesFrom=[]
        self.languagesTo=[]
        languages=[]
        for k, v in langForTran.iteritems():
            languages.append(v)
        countItem=0
        languages.sort()
        languagesCopy=list(languages)
        for s in languagesCopy:
            if s in options.langList:
                languages.remove(s)
                languages.insert(countItem,s)
                countItem+=1
            if countItem == len(options.langList):
                languages.insert(countItem,"--------")
                break

        self.languagesTo=languages
        self.languagesFrom=['Auto']+languages
        self.view.t_choiceLangFrom.SetItems(self.languagesFrom)
        self.view.t_choiceLangFrom.Selection=self.languagesFrom.index(options.defaultLangFrom)
        self.view.t_choiceLangTo.SetItems(self.languagesTo)
        self.view.t_choiceLangTo.Selection = self.languagesTo.index(options.defaultLangTo)

    def hide_controls(self):
        """
        hide controls when start translate
        """
        self.view.ag.Show(True)
        self.view.t_textCtrl.Hide()
        self.view.t_choiceLangFrom.Hide()
        self.view.t_bitmapArrow.Hide()
        self.view.t_choiceLangTo.Hide()
        self.view.t_bitmapCopy.Hide()
        self.view.m_bitmapClose.Hide()

    def show_controls(self):
        """
        show controls if having translate result
        """
#        print "show controls"
        self.view.t_textCtrl.Show(True)
        self.view.t_bitmapArrow.Show(True)
        self.view.t_choiceLangFrom.Show(True)
        self.view.t_choiceLangTo.Show(True)
        self.view.t_bitmapCopy.Show(True)
        self.view.m_bitmapClose.Show(True)
        self.view.ag.Hide()


    def show_error_controls(self):
        """
        show controls when result translate with error
        """
        self.view.t_textCtrl.Show(True)
        self.view.m_bitmapClose.Show(True)
        self.view.ag.Hide()

    def set_position(self):
        """
        set frame position
        """
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
#        print "set_position"

    def set_size(self,dataText):
        """
        set frame size
        """
        if '----' in dataText:
            self.view.SetSize((285,100+len(dataText)*0.2))
        elif len(dataText)<=1500:
            width=285+len(dataText)/2.5
            height=80+len(dataText)*0.2
            if width>500: width=500
            if height>400:height=400
            self.view.SetSize((width,height))
        elif len(dataText)>1500:
            self.view.SetSize((500,400))

    def on_mouse_left_down(self, evt):
        self.ldPos = evt.GetEventObject().ClientToScreen(evt.GetPosition())
        self.wPos = self.view.ClientToScreen((0,0))

    def event_motion(self, event):
        """
        motion frame
        """
        if event.Dragging() and event.LeftIsDown():
            dPos = event.GetEventObject().ClientToScreen(event.GetPosition())
            nPos = (self.wPos.x + (dPos.x - self.ldPos.x),
                    self.wPos.y + (dPos.y - self.ldPos.y))
            self.view.Move(nPos)
        event.Skip()

    def event_choice_lang_to( self, event ):
        self.choice_lang()

    def event_choice_lang_from( self, event ):
        self.choice_lang()

    def choice_lang(self):
        """
        start alternative translate, when choice other language
        """
        langFrom=self.languagesFrom[self.view.t_choiceLangFrom.Selection]
        langTo=self.languagesTo[self.view.t_choiceLangTo.Selection]
        if langFrom == "--------":
            self.view.t_choiceLangFrom.Selection -= 1
            langFrom=self.languagesFrom[self.view.t_choiceLangFrom.Selection]
        if langTo == "--------":
            self.view.t_choiceLangTo.Selection -= 1
            langTo=self.languagesTo[self.view.t_choiceLangTo.Selection]
        options.countClickUp=2
        self.hide_controls()
        self.view.SetSize((50,17))
        self.view.Layout()
        self.start_translate(langFrom,langTo)


    def event_select_lang( self, event ):
        """
        set bool data in selectLang for know, hide frame when mouse event outside frames or not
        """
        self.view.selectLang=True
        event.Skip()

    def event_deselect_lang( self, event ):
        """
        the same as event_select_lang
        """

        self.view.selectLang=False
        event.Skip()

    def event_copy( self, event ):
        """
        copy translated text
        """
        data = wx.TextDataObject()
        data.SetText(self.translatedText)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox(_("Unable to open the clipboard"), _("Error"))
        options.isRunTranslate=False
        self.view.Hide()

    def event_close( self, event ):
        """
        hide frame
        """
#        print "close result"
        options.isRunTranslate=False
        self.view.Hide()

    def update_display(self, msg):
        """
        Receives data from thread and updates the frame
        """
        options.isRunTranslate=False
        if msg.data[2]==self.countRunTranslator:
            lang=''
            if self.view.t_choiceLangFrom.GetStringSelection() == 'Auto':
                for k, v in langForTran.iteritems():
                        if k==msg.data[0]:
                            lang=v
                self.view.t_textCtrl.SetValue(msg.data[1]+'\n('+_('Source lang is ') +lang+')')
            else: self.view.t_textCtrl.SetValue(msg.data[1])

            self.translatedText=msg.data[1]
            self.show_controls()
            self.set_size(msg.data[1])
            self.set_position()
            self.countRunTranslator=0


