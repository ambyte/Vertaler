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

""" Notification about new version """
import webbrowser
import wx
from src.modules.settings import options

class NotificationFrame ( wx.Frame ):

    def __init__( self, parent,version ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString,
                            pos = wx.DefaultPosition, size = wx.Size( 299,156 ),
                            style = wx.NO_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP )

        cursor = wx.StockCursor(wx.CURSOR_HAND)
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Vertaler", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 15, 70, 90, 92, False, wx.EmptyString ) )

        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, _("Available the new version")+
                               ' Vertaler '+str(version), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        self.m_staticText3.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )

        bSizer2.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _("you can download and install it"),
                                            wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        self.m_staticText2.SetFont( wx.Font( 10, 70, 90, 90, False, wx.EmptyString ) )

        bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_hyperlink1 = wx.HyperlinkCtrl( self, wx.ID_ANY, u"www.vertalerproject.org",
                                              u"http://vertaler.weebly.com/downloads.html",
                                              wx.DefaultPosition, wx.DefaultSize, wx.HL_DEFAULT_STYLE )
        bSizer2.Add( self.m_hyperlink1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer1.Add( bSizer2, 5, wx.EXPAND, 5 )

        bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, _("Don't show again"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_checkBox1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/delete_icon&16.png", wx.BITMAP_TYPE_ANY ),
                                          wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_bitmap1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        self.m_bitmap1.SetCursor(cursor)

        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_bitmap1.Bind( wx.EVT_LEFT_DOWN, self.event_close )
        self.m_hyperlink1.Bind( wx.EVT_LEFT_DOWN, self.event_hyperlink )
        self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.event_check )

    # Virtual event handlers, overide them in your derived class
    def event_close( self, event ):
        self.Hide()
        self.Destroy()

    def event_hyperlink( self, event ):
        webbrowser.open_new_tab(self.m_hyperlink1.GetURL())
        self.Hide()
        self.Destroy()

    def event_check( self, event ):
        options.enableNotification=not self.m_checkBox1.IsChecked()