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

import wx
from src.modules import gettext_windows
from src.modules import options


class PopUpFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 112,24 ), style = wx.NO_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP )

        cursor = wx.StockCursor(wx.CURSOR_HAND)


        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        bSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.p_bitmapTranslate = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/refresh_icon&16.png", wx.BITMAP_TYPE_ANY ),
                                                  wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_bitmapTranslate.SetToolTipString( _("Translate text") )
        self.p_bitmapTranslate.SetCursor(cursor)


        bSizer.Add( self.p_bitmapTranslate, 0, wx.ALL, 3 )

        self.p_bitmapCopy = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/clipboard_copy_icon&16.png",
            wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_bitmapCopy.SetToolTipString( _("Copy text") )
        self.p_bitmapCopy.SetCursor(cursor)

        bSizer.Add( self.p_bitmapCopy, 0, wx.ALL, 3 )

        self.p_bitmapSearch = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/zoom_icon&16.png", wx.BITMAP_TYPE_ANY ),
                                               wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_bitmapSearch.SetToolTipString( _("Search") )
        self.p_bitmapSearch.SetCursor(cursor)

        bSizer.Add( self.p_bitmapSearch, 0, wx.ALL, 3 )

        self.p_bitmapOpenMain = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/home_icon&16.png", wx.BITMAP_TYPE_ANY ),
                                                 wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_bitmapOpenMain.SetToolTipString( _("Open main window") )
        self.p_bitmapOpenMain.SetCursor(cursor)

        bSizer.Add( self.p_bitmapOpenMain, 0, wx.ALL, 3 )

        self.p_bitmapClose = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe//delete_icon&16.png", wx.BITMAP_TYPE_ANY ),
                                              wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_bitmapClose.SetToolTipString( _("Close") )
        self.p_bitmapClose.SetCursor(cursor)

        bSizer.Add( self.p_bitmapClose, 0, wx.ALL, 3 )

        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.SetSizer( bSizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__(self):
        pass
