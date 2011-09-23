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

""" Controller for Setting frame """

import os
import wx
from src.views.settingframe import SettingFrame
import src.modules.options as options
from src.views.settingframeforposix import SettingFrameForPosix

if os.name =="nt":
    from src.modules import startupapp
from wx.lib.pubsub import Publisher as pub
from src.modules import gettext_windows

class SettingController:
    def __init__(self):
        if os.name =="nt":
            self.view = SettingFrame(None)
        elif os.name =="posix":
            self.view = SettingFrameForPosix(None)
        self.view.s_staticTextMessage.Label=""
        if options.useControl:
            self.view.s_radioBox1.SetSelection(0)
        if options.useNothing:
            self.view.s_radioBox1.SetSelection(1)
        if options.useGoogle:
            self.view.s_radioBox2.SetSelection(1)
        if options.useBing:
            self.view.s_radioBox2.SetSelection(0)

        self.view.s_choiceSearch.Selection=options.defaultSearchEngine
        self.view.s_checkBoxDblCtrl.SetValue(options.useDblControl)
        if os.name =="nt":
            self.view.s_checkBoxStartWithWin.SetValue(options.startWithOS)
            self.view.s_checkBoxUseProxy.SetValue(options.useProxy)
            self.view.s_textCtrlAddress.Value=options.proxyAddress
            self.view.s_textCtrlPort.Value=options.proxyPort
            self.view.s_textCtrlLogin.Value=options.proxyLogin
            self.view.s_textCtrlPass.Value=options.proxyPassword
            self.view.s_checkBoxUpdate.SetValue(options.enableNotification)

        # Connect Events

        self.view.s_buttonCancel.Bind( wx.EVT_BUTTON, self.event_cancel)
        self.view.s_buttonSave.Bind( wx.EVT_BUTTON, self.event_save )
        self.view.ShowModal()
        self.view.Destroy()

    def event_cancel( self, event ):
        self.view.Close()

    def event_save( self, event ):
        if os.name =="nt" and self.view.s_checkBoxUseProxy.GetValue():
            if self.view.s_textCtrlPort.Value=="" and self.view.s_textCtrlAddress.Value=="":
                self.view.s_staticTextMessage.Label=_("Inter address and port for proxy")
                return 0
            if self.view.s_textCtrlAddress.Value=="":
                self.view.s_staticTextMessage.Label=_("Inter address for proxy")
                return 0
            if self.view.s_textCtrlPort.Value=="":
                self.view.s_staticTextMessage.Label=_("Inter port for proxy")
                return 0

        radioIndex2 =self.view.s_radioBox2.GetSelection()
        if not radioIndex2:
            options.useGoogle=False
            options.useBing=True
        elif radioIndex2:
            options.useGoogle=True
            options.useBing=False
        radioIndex1 =self.view.s_radioBox1.GetSelection()
        if not radioIndex1:
            options.useControl=True
            options.useNothing=False
        elif radioIndex1:
            options.useControl=False
            options.useNothing=True
        options.defaultSearchEngine=self.view.s_choiceSearch.Selection
        options.useDblControl=self.view.s_checkBoxDblCtrl.GetValue()

        if os.name =="nt":
            options.enableNotification=self.view.s_checkBoxUpdate.GetValue()
            options.useProxy=self.view.s_checkBoxUseProxy.GetValue()
            options.proxyAddress=self.view.s_textCtrlAddress.Value
            options.proxyPort=self.view.s_textCtrlPort.Value
            options.proxyLogin=self.view.s_textCtrlLogin.Value
            options.proxyPassword=self.view.s_textCtrlPass.Value
            options.startWithOS=self.view.s_checkBoxStartWithWin.GetValue()
            self.start_with_os()

        pub.sendMessage("SAVE SETTINGS")
        self.view.Close()

    def start_with_os(self):
        if os.name =="nt":
            if options.startWithOS:
                startupapp.set_startup()
            else:
                startupapp.delete_startup()




