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
from src.gui.settingframe import SettingFrame
import src.modules.settings.config as options
from src.gui.settingframeforposix import SettingFrameForPosix

if os.name =="nt":
    from src.modules import startupapp
from wx.lib.pubsub import pub

class SettingController:
    def __init__(self):
        if os.name =="nt":
            self.view = SettingFrame(None)
        elif os.name =="posix":
            self.view = SettingFrameForPosix(None)
        self.view.s_staticTextMessage.Label=""
        if config.useControl:
            self.view.s_radioBox1.SetSelection(0)
        if config.useNothing:
            self.view.s_radioBox1.SetSelection(1)
        if config.useGoogle:
            self.view.s_radioBox2.SetSelection(1)
        if config.useBing:
            self.view.s_radioBox2.SetSelection(0)

        self.view.s_choiceSearch.Selection= config.defaultSearchEngine
        self.view.s_checkBoxDblCtrl.SetValue(config.useDblControl)
        if os.name =="nt":
            self.view.s_checkBoxStartWithWin.SetValue(config.startWithOS)
            self.view.s_checkBoxUseProxy.SetValue(config.useProxy)
            self.view.s_textCtrlAddress.Value= config.proxyAddress
            self.view.s_textCtrlPort.Value= config.proxyPort
            self.view.s_textCtrlLogin.Value= config.proxyLogin
            self.view.s_textCtrlPass.Value= config.proxyPassword
            self.view.s_checkBoxUpdate.SetValue(config.enableNotification)

        # Connect Events

        self.view.s_buttonCancel.Bind( wx.EVT_BUTTON, self.event_cancel)
        self.view.s_buttonSave.Bind( wx.EVT_BUTTON, self.event_save )
        self.view.ShowModal()
        self.view.Destroy()

    def event_cancel( self, event ):
        self.view.Close()

    def event_save( self, event ):
        publisher = pub.Publisher()
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
            config.useGoogle=False
            config.useBing=True
        elif radioIndex2:
            config.useGoogle=True
            config.useBing=False
        radioIndex1 =self.view.s_radioBox1.GetSelection()
        if not radioIndex1:
            config.useControl=True
            config.useNothing=False
        elif radioIndex1:
            config.useControl=False
            config.useNothing=True
        config.defaultSearchEngine=self.view.s_choiceSearch.Selection
        config.useDblControl=self.view.s_checkBoxDblCtrl.GetValue()

        if os.name =="nt":
            config.enableNotification=self.view.s_checkBoxUpdate.GetValue()
            config.useProxy=self.view.s_checkBoxUseProxy.GetValue()
            config.proxyAddress=self.view.s_textCtrlAddress.Value
            config.proxyPort=self.view.s_textCtrlPort.Value
            config.proxyLogin=self.view.s_textCtrlLogin.Value
            config.proxyPassword=self.view.s_textCtrlPass.Value
            config.startWithOS=self.view.s_checkBoxStartWithWin.GetValue()
            self.start_with_os()

        publisher.sendMessage("SAVE SETTINGS")
        self.view.Close()

    def start_with_os(self):
        if os.name =="nt":
            if config.startWithOS:
                startupapp.set_startup()
            else:
                startupapp.delete_startup()




