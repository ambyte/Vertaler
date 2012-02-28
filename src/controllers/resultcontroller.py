# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
import wx
from src.modules.settings import config
from src.modules.translateservices import translatethread
from src.gui.resultframe import ResultFrame
from src.modules.settings.config import langForTran

if os.name =="nt":
    import win32gui
    from src.modules import clipboardlib
elif os.name =="posix":
    from Xlib import display
from wx.lib.pubsub import pub


class ResultController:

    def __init__(self):
         publisher = pub.Publisher()
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
         publisher.subscribe(self.update_display, "TRANSLATE")

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
            self.start_translate(config.defaultLangFrom, config.defaultLangTo)
        else:
            if os.name =="nt":
                clipboardlib.event_press_ctrl()
            config.isRunTranslate=False

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
            if s in config.langList:
                languages.remove(s)
                languages.insert(countItem,s)
                countItem+=1
            if countItem == len(config.langList):
                languages.insert(countItem,"--------")
                break

        self.languagesTo=languages
        self.languagesFrom=['Auto']+languages
        self.view.t_choiceLangFrom.SetItems(self.languagesFrom)
        self.view.t_choiceLangFrom.Selection=self.languagesFrom.index(config.defaultLangFrom)
        self.view.t_choiceLangTo.SetItems(self.languagesTo)
        self.view.t_choiceLangTo.Selection = self.languagesTo.index(config.defaultLangTo)

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
        width=315+len(dataText)/2.5
        self.view.SetSize((width,100))
        numLines=self.view.t_textCtrl.GetNumberOfLines()
        w,h = self.view.t_textCtrl.GetTextExtent(dataText)
        height=numLines*h+45
        if width > 500: width=500
        if height > 400: height=400
        self.view.SetSize((width,height))

    def GetLineHeight(self,rtc,tallString):
#        rtc.SetInsertionPoint(0)
#        rtc.PageDown()
#        pos = rtc.GetInsertionPoint()
#        end = tallString.find("\n",pos)
##        lineHeight=int(tallString[pos+2:end])
#        lineHeight=end-pos
#        return lineHeight
        tallString = "\n".join([str(i) for i in xrange(200)])
        rtc.SetValue(tallString)
        rtc.SetInsertionPoint(0)
        rtc.PageDown()
        pos = rtc.GetInsertionPoint()
        end = tallString.find("\n",pos)
        lineHeight=int(tallString[pos:end])
        return lineHeight

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
        config.countClickUp=2
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
        config.isRunTranslate=False
        self.view.Hide()

    def event_close( self, event ):
        """
        hide frame
        """
#        print "close result"
        config.isRunTranslate=False
        self.view.Hide()

    def update_display(self, msg):
        """
        Receives data from thread and updates the frame
        """

        if config.useGoogle:
            config.isRunTranslate=False
            tranText=msg.data[1][0][0]
            ishText=msg.data[1][0][1]
            latTranText=msg.data[1][0][2]
            latIshText=msg.data[1][0][3]
            dTranText=""
            translatedText=""
            try:
                for text in  msg.data[1][1]:
                    dTranText+=text+" "
            except Exception:
                pass

            if msg.data[len(msg.data)-1]==self.countRunTranslator:
                lang=''
                if self.view.t_choiceLangFrom.GetStringSelection() == 'Auto':
                    for k, v in langForTran.iteritems():
                        if k==msg.data[0]:
                            lang=v
                    if dTranText!="":
                        translatedText=tranText+'\n--------------\n'+dTranText+'\n-------------\n('+_('Source lang is ') +lang+')'
                        self.view.t_textCtrl.SetValue(tranText+'\n--------------\n'+dTranText+'\n-------------\n('+_('Source lang is ') +lang+')')
                    else:
                        translatedText=tranText+'\n-------------\n('+_('Source lang is ') +lang+')'
                        self.view.t_textCtrl.SetValue(tranText+'\n-------------\n('+_('Source lang is ') +lang+')')
                else: self.view.t_textCtrl.SetValue(tranText)

                self.translatedText=msg.data[1][0][0]
                self.show_controls()
                self.set_size(translatedText)
                self.set_position()
                self.countRunTranslator=0
        else:
            config.isRunTranslate=False
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

