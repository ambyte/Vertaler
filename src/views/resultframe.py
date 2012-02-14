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
import wx.animate
from src.modules.settings import options

class ResultFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, size = wx.Size( 50,17 ),
                            style = wx.NO_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP )

        cursor = wx.StockCursor(wx.CURSOR_HAND)

        self.selectLang=False
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        self.bSizer = wx.BoxSizer( wx.VERTICAL )

        bSizerText = wx.BoxSizer( wx.HORIZONTAL )

        self.t_textCtrl = wx.TextCtrl( self, id=wx.ID_ANY, value=wx.EmptyString,
                                       style=wx.TE_MULTILINE|wx.TE_RICH|wx.NO_BORDER|wx.TRANSPARENT_WINDOW )
        bSizerText.Add( self.t_textCtrl, 1, wx.ALL|wx.EXPAND, 5 )

        self.bSizer.Add( bSizerText, 7, wx.EXPAND, 0 )

        bSizerButtons = wx.BoxSizer( wx.HORIZONTAL )

        ag_fname = "./src/icons/popupframe/ajax-loader.gif"
        self.ag = wx.animate.GIFAnimationCtrl(self, wx.ID_ANY, ag_fname, wx.DefaultPosition)
        # clears the background
        self.ag.GetPlayer().UseBackgroundColour(False)
        # continuously loop through the frames of the gif file (default)
        self.ag.Play()
        bSizerButtons.Add( self.ag, 0, wx.ALIGN_CENTER|wx.ALL, 3 )

        self.t_choiceLangFrom = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(90,-1), [], 0 )
        bSizerButtons.Add( self.t_choiceLangFrom, 0, wx.ALIGN_CENTER|wx.ALL, 6 )

        self.t_bitmapArrow = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/arrow_right_12x12.png",
                                                      wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )

        bSizerButtons.Add( self.t_bitmapArrow, 0,wx.ALIGN_CENTER|wx.ALL, 6 )

        t_choiceLangToChoices = []
        self.t_choiceLangTo = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(90,-1), t_choiceLangToChoices, 0 )
        self.t_choiceLangTo.SetSelection( 0 )
        bSizerButtons.Add( self.t_choiceLangTo, 0, wx.ALIGN_CENTER|wx.ALL, 6 )


        self.t_bitmapCopy = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/clipboard_copy_icon&16.png",
                                                         wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.t_bitmapCopy.SetToolTipString( u"Copy text" )
        self.t_bitmapCopy.SetCursor(cursor)
        bSizerButtons.Add( self.t_bitmapCopy, 0,wx.ALIGN_CENTER|wx.ALL, 6 )

        self.m_bitmapClose = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/popupframe/delete_icon&16.png",
                                                      wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_bitmapClose.SetToolTipString( u"Close" )
        self.m_bitmapClose.SetCursor(cursor)

        bSizerButtons.Add( self.m_bitmapClose, 0, wx.ALIGN_CENTER|wx.ALL, 6 )

        self.bSizer.Add( bSizerButtons, 0, wx.ALIGN_RIGHT, 6 )

        self.SetSizer( self.bSizer )
        self.Layout()

    def __del__(self):
        pass


