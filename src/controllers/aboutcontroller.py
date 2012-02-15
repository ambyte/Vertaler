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

""" Controller for AboutBox frame """

import wx
from src.modules.settings import config
from src.gui.aboutframe import AboutFrame, licence
from wx.lib.pubsub import pub
from src.modules import  getnewversion


description = _('Vertaler is an open source program that allows you to translate the text in a variety\
 of applications using Google Translate and Bing Translator services')
icons = _('Some icons are taken from libraries: ')
newVersion=_('Available the new version')
copyright = '(C) 2011 Sergey Gulyaev'

class AboutController:
    def __init__(self):
        publisher = pub.Publisher()
        self.view = AboutFrame(None, _('About Vertaler'))
        newVersion=getnewversion.NewVersionThread(True)
        publisher.subscribe(self.version_result, "VERSION ABOUT")
        self.page = '''<html>
        <h1 align="center">Vertaler %s</h1>
        <p align="center">"%s"</p>
        <p align="center">"%s"</p>
        <p align="center"><a href="www.vertalerproject.com">www.vertalerproject.com</a></p>
        <p align="center">"%s"</p>
        <p align="center"><a href="http://openiconlibrary.sourceforge.net/">Open Icon Library</a></p>
        <p align="center"><a href="http://gentleface.com/free_icon_set.html">Wireframe Toolbar Icons</a></p>
        </html>''' % (config.version,description.encode("UTF-8"),copyright,icons.encode("UTF-8"))
        self.view.b_htmlWin.SetPage(self.page.decode("UTF-8"))

        # Connect Events
        self.view.b_buttonClose.Bind( wx.EVT_LEFT_DOWN, self.event_close )
        self.view.b_buttonLicense.Bind( wx.EVT_LEFT_DOWN, self.event_license )

        self.view.ShowModal()
        self.view.Destroy()

    def event_close( self, event ):
        self.view.Close()

    def event_license( self, event ):
        if self.view.b_buttonLicense.Label==_('License'):
            self.view.b_htmlWin.SetPage(licence.decode("UTF-8"))
            self.view.b_buttonLicense.Label=_('< About')
        else:
            self.view.b_htmlWin.SetPage(self.page.decode("UTF-8"))
            self.view.b_buttonLicense.Label=_('License')

    def version_result(self, msg):
        if config.version < msg.data:
            try:
                if config.version < msg.data:
                    self.page = '''<html>
                    <h1 align="center">Vertaler %s</h1>
                    <p align="center">%s</p>
                    <p align="center">%s</p>
                    <p align="center">%s Vertaler %s</p>
                    <p align="center"><a href="www.vertalerproject.com">www.vertalerproject.com</a></p>
                    <p align="center">%s</p>
                    <p align="center"><a href="http://openiconlibrary.sourceforge.net/">Open Icon Library</a></p>
                    <p align="center"><a href="http://gentleface.com/free_icon_set.html">Wireframe Toolbar Icons</a></p>
                    </html>''' % (config.version,description.encode("UTF-8"),copyright,
                                      newVersion.encode("UTF-8"),msg.data,icons.encode("UTF-8"))
            except Exception, ex:
                pass
            self.view.b_htmlWin.SetPage(self.page.decode("UTF-8"))

