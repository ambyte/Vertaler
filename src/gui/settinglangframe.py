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
import os

import wx
from src.modules import gettext_windows

class SettingLangFrame ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Choice favorite languages"),
                             pos = wx.DefaultPosition, size = wx.Size( 220,253 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        lSizer = wx.BoxSizer( wx.VERTICAL )

        lSizerSearch = wx.BoxSizer( wx.VERTICAL )

        self.l_searchCtrl = wx.SearchCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_searchCtrl.ShowSearchButton( True )
        self.l_searchCtrl.ShowCancelButton( True )
        lSizerSearch.Add( self.l_searchCtrl, 0, wx.ALL|wx.EXPAND, 5 )

        lSizer.Add( lSizerSearch, 0, wx.EXPAND, 5 )

        lSizerCheckList = wx.BoxSizer( wx.VERTICAL )

        self.l_checkList = wx.CheckListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, [], 0 )
        lSizerCheckList.Add( self.l_checkList, 1, wx.ALL|wx.EXPAND, 5 )

        lSizer.Add( lSizerCheckList, 1, wx.EXPAND, 5 )

        lSizerButtons = wx.BoxSizer( wx.HORIZONTAL )

        self.l_buttonSave = wx.Button( self, wx.ID_ANY, _("Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
        lSizerButtons.Add( self.l_buttonSave, 0, wx.ALL, 5 )

        self.l_buttonCancel = wx.Button( self, wx.ID_ANY, _("Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        lSizerButtons.Add( self.l_buttonCancel, 0, wx.ALL, 5 )

        lSizer.Add( lSizerButtons, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.SetSizer( lSizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__(self):
        pass

