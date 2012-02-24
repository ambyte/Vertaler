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
from src.modules.settings import config

class Settings():
    def __init__(self):
        self.cfg = wx.Config('vertalerconfig')
#        self.initialization_config()

    def initialization_config(self):
        if self.cfg.Exists('langList'):
            data = self.cfg.Read("langList")
            data=str(unicode(data))
            if cPickle.loads(data):
                config.langList = cPickle.loads(data)

        if self.cfg.Exists('defaultLangFrom'):
            data = self.cfg.Read("defaultLangFrom")
            config.defaultLangFrom=str(unicode(data))
        if self.cfg.Exists('defaultLangTo'):
            data = self.cfg.Read("defaultLangTo")
            config.defaultLangTo=str(unicode(data))

        if self.cfg.Exists('enableNotification'):
            config.enableNotification  = self.cfg.ReadBool("enableNotification")
        if self.cfg.Exists('visitedVersion'):
            config.visitedVersion = self.cfg.ReadFloat("visitedVersion")
        if self.cfg.Exists('defaultSearchEngine'):
            config.defaultSearchEngine = self.cfg.ReadInt("defaultSearchEngine")
        if self.cfg.Exists('useControl'):
            config.useControl = self.cfg.ReadBool("useControl")
        if self.cfg.Exists('useDblControl'):
            config.useDblControl = self.cfg.ReadBool("useDblControl")
        if self.cfg.Exists('useNothing'):
            config.useNothing = self.cfg.ReadBool("useNothing")
        if self.cfg.Exists('useGoogle'):
            config.useGoogle = self.cfg.ReadBool("useGoogle")
        if self.cfg.Exists('useBing'):
            config.useBing = self.cfg.ReadBool("useBing")
        if self.cfg.Exists('startWithOS'):
            config.startWithOS = self.cfg.ReadBool("startWithOS")
        if self.cfg.Exists('useProxy'):
            config.useProxy = self.cfg.ReadBool("useProxy")
        if self.cfg.Exists('proxyAddress'):
            data = self.cfg.Read("proxyAddress")
            config.proxyAddress=str(unicode(data))
        if self.cfg.Exists('proxyPort'):
            data = self.cfg.Read("proxyPort")
            config.proxyPort=str(unicode(data))
        if self.cfg.Exists('proxyLogin'):
            data = self.cfg.Read("proxyLogin")
            config.proxyLogin=str(unicode(data))
        if self.cfg.Exists('proxyPassword'):
            data = self.cfg.Read("proxyPassword")
            config.proxyPassword=str(unicode(data))
        if self.cfg.Exists('isFirstStart'):
            config.isFirstStart = self.cfg.ReadBool("isFirstStart")
        return True

    def set_global_params(self):
        langList =  cPickle.dumps(config.langList)
        if config.enableApp:
            self.cfg.WriteBool("useControl", config.useControl)
            self.cfg.WriteBool("useNothing", config.useNothing)
        self.cfg.WriteFloat("visitedVersion", config.visitedVersion)
        self.cfg.WriteInt("defaultSearchEngine", config.defaultSearchEngine)
        self.cfg.WriteBool("useDblControl", config.useDblControl)
        self.cfg.WriteBool("enableNotification", config.enableNotification)
        self.cfg.Write("langList", langList)
        self.cfg.WriteBool("useGoogle", config.useGoogle)
        self.cfg.WriteBool("useBing", config.useBing)
        self.cfg.WriteBool("useProxy", config.useProxy)
        self.cfg.WriteBool("startWithOS", config.startWithOS)
        self.cfg.Write("proxyAddress", config.proxyAddress)
        self.cfg.Write("proxyPort", config.proxyPort)
        self.cfg.Write("proxyLogin", config.proxyLogin)
        self.cfg.Write("proxyPassword", config.proxyPassword)
        self.cfg.Write("defaultLangFrom", config.defaultLangFrom)
        self.cfg.Write("defaultLangTo", config.defaultLangTo)
        self.cfg.WriteBool("isFirstStart", config.isFirstStart)
        self.cfg.Flush()

    def save_lang_param(self):
        self.cfg.Write("defaultLangFrom", config.defaultLangFrom)
        self.cfg.Write("defaultLangTo", config.defaultLangTo)
        langList =  cPickle.dumps(config.langList)
        self.cfg.Write("langList", langList)

