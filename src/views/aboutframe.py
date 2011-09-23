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

import webbrowser
import wx
import wx.html
from src.modules import gettext_windows


licence = '''
<h1 align="center">Lisense</h1>
<p align="center">
Copyright (c) 2011 Sergey Gulyaev <astraway@gmail.com>
</p>

<p align="center">
All rights reserved.
</p>

<p>
Vertaler is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
</p>

 <p align="justify">
Vertaler is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Library General Public License for more details.
</p>

<p align="justify">
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
</p>
'''


class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         webbrowser.open(link.GetHref())

class AboutFrame ( wx.Dialog ):

    def __init__(self, parent, title):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( 427,309 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer = wx.BoxSizer( wx.VERTICAL )

        bSizerHtmlWindow = wx.BoxSizer( wx.VERTICAL )

        self.b_htmlWin = wxHTML( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.html.HW_NO_SELECTION|wx.html.HW_SCROLLBAR_AUTO )
        bSizerHtmlWindow.Add( self.b_htmlWin, 1, wx.ALL|wx.EXPAND, 5 )
#        self.b_htmlWin.SetPage(page.decode("UTF-8"))

        bSizer.Add( bSizerHtmlWindow, 1, wx.EXPAND, 5 )



        bSizerButtons = wx.BoxSizer( wx.HORIZONTAL )

        bSizerButtonLicense = wx.BoxSizer( wx.VERTICAL )

        self.b_buttonLicense = wx.Button( self, wx.ID_ANY, _("License"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerButtonLicense.Add( self.b_buttonLicense, 0, wx.ALL, 5 )

        bSizerButtons.Add( bSizerButtonLicense, 1, wx.EXPAND|wx.ALIGN_BOTTOM, 5 )

        bSizerButtonClose = wx.BoxSizer( wx.VERTICAL )

        self.b_buttonClose = wx.Button( self, wx.ID_ANY, _("Close"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerButtonClose.Add( self.b_buttonClose, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )

        bSizerButtons.Add( bSizerButtonClose, 1, wx.EXPAND|wx.ALIGN_BOTTOM, 5 )

        bSizer.Add( bSizerButtons, 0, wx.EXPAND, 5 )

        self.SetSizer( bSizer )
        self.Layout()

        self.Centre( wx.BOTH )
