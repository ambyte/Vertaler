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

""" Save and load settings """

import wx
import cPickle
from src.modules import options

class Settings():
    def __init__(self):
        self.cfg = wx.Config('vertalerconfig')
        self.initialization_config()

    def initialization_config(self):
        if self.cfg.Exists('langList'):
            data = self.cfg.Read("langList")
            data=str(unicode(data))
            if cPickle.loads(data):
                options.langList = cPickle.loads(data)

        if self.cfg.Exists('defaultLangFrom'):
            data = self.cfg.Read("defaultLangFrom")
            options.defaultLangFrom=str(unicode(data))
        if self.cfg.Exists('defaultLangTo'):
            data = self.cfg.Read("defaultLangTo")
            options.defaultLangTo=str(unicode(data))

        if self.cfg.Exists('enableNotification'):
            options.enableNotification  = self.cfg.ReadBool("enableNotification")
        if self.cfg.Exists('visitedVersion'):
            options.visitedVersion = self.cfg.ReadFloat("visitedVersion")
        if self.cfg.Exists('defaultSearchEngine'):
            options.defaultSearchEngine = self.cfg.ReadInt("defaultSearchEngine")
        if self.cfg.Exists('useControl'):
            options.useControl = self.cfg.ReadBool("useControl")
        if self.cfg.Exists('useDblControl'):
            options.useDblControl = self.cfg.ReadBool("useDblControl")
        if self.cfg.Exists('useNothing'):
            options.useNothing = self.cfg.ReadBool("useNothing")
        if self.cfg.Exists('useGoogle'):
            options.useGoogle = self.cfg.ReadBool("useGoogle")
        if self.cfg.Exists('useBing'):
            options.useBing = self.cfg.ReadBool("useBing")
        if self.cfg.Exists('startWithOS'):
            options.startWithOS = self.cfg.ReadBool("startWithOS")
        if self.cfg.Exists('useProxy'):
            options.useProxy = self.cfg.ReadBool("useProxy")
        if self.cfg.Exists('proxyAddress'):
            data = self.cfg.Read("proxyAddress")
            options.proxyAddress=str(unicode(data))
        if self.cfg.Exists('proxyPort'):
            data = self.cfg.Read("proxyPort")
            options.proxyPort=str(unicode(data))
        if self.cfg.Exists('proxyLogin'):
            data = self.cfg.Read("proxyLogin")
            options.proxyLogin=str(unicode(data))
        if self.cfg.Exists('proxyPassword'):
            data = self.cfg.Read("proxyPassword")
            options.proxyPassword=str(unicode(data))
        return True

    def set_global_params(self):
        langList =  cPickle.dumps(options.langList)
        if options.enableApp:
            self.cfg.WriteBool("useControl", options.useControl)
            self.cfg.WriteBool("useNothing", options.useNothing)
        self.cfg.WriteFloat("visitedVersion", options.visitedVersion)
        self.cfg.WriteInt("defaultSearchEngine", options.defaultSearchEngine)
        self.cfg.WriteBool("useDblControl", options.useDblControl)
        self.cfg.WriteBool("enableNotification", options.enableNotification)
        self.cfg.Write("langList", langList)
        self.cfg.WriteBool("useGoogle", options.useGoogle)
        self.cfg.WriteBool("useBing", options.useBing)
        self.cfg.WriteBool("useProxy", options.useProxy)
        self.cfg.WriteBool("startWithOS", options.startWithOS)
        self.cfg.Write("proxyAddress", options.proxyAddress)
        self.cfg.Write("proxyPort", options.proxyPort)
        self.cfg.Write("proxyLogin", options.proxyLogin)
        self.cfg.Write("proxyPassword", options.proxyPassword)
        self.cfg.Write("defaultLangFrom", options.defaultLangFrom)
        self.cfg.Write("defaultLangTo", options.defaultLangTo)
        self.cfg.Flush()

    def save_lang_param(self):
        self.cfg.Write("defaultLangFrom", options.defaultLangFrom)
        self.cfg.Write("defaultLangTo", options.defaultLangTo)
        langList =  cPickle.dumps(options.langList)
        self.cfg.Write("langList", langList)

