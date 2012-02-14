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

""" Controller for TaskBar """
import wx
from src.controllers import settingcontroller, aboutcontroller
from src.modules.settings import options

from src.views.mainframe import MainTaskBarIcon

class MainTaskBarIconController:

    def __init__(self):
         self.tbicon = MainTaskBarIcon(self)

         self.tbicon.menuItemCtrl.Check(options.useControl)
         self.tbicon.menuItemNothing.Check(options.useNothing)

         # Connect Events

         self.tbicon.Bind( wx.EVT_MENU,self.event_about, self.tbicon.menuAbout  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_settings, self.tbicon.menuSetting  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_setting_ctrl, self.tbicon.menuItemCtrl  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_setting_nothing, self.tbicon.menuItemNothing  )

    def event_setting_ctrl( self, event ):
        """
        translate text when press control
        """
        options.useControl=self.tbicon.menuItemCtrl.IsChecked()

    def event_setting_nothing( self, event ):
        """
        translate text when nothing press
        """
        options.useNothing=self.tbicon.menuItemNothing.IsChecked()

    def event_about( self, event ):
        """
        Open about frame
        """
        aboutcontroller.AboutController()

    def event_settings(self, event):
        """
        Open settings
        """
        settingcontroller.SettingController()

  