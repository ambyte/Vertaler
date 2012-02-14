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
from src.modules.settings import options

class SettingFrameForPosix ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _("Settings"), pos = wx.DefaultPosition,
                             size = wx.Size( 500,300 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizerMain = wx.BoxSizer( wx.VERTICAL )

        bSizerSetting = wx.BoxSizer( wx.VERTICAL )

        bSizerLeft = wx.BoxSizer( wx.VERTICAL )

        sbSizerRadioButtons = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.HORIZONTAL )

        s_radioBox1Choices = [ u"Control", _("Nothing") ]
        self.s_radioBox1 = wx.RadioBox( self, wx.ID_ANY, _("Use keyboard button"), wx.DefaultPosition,
                                        wx.Size( 160,-1 ), s_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
        sbSizerRadioButtons.Add( self.s_radioBox1, 0, wx.ALL|wx.EXPAND, 5 )

        s_radioBox2Choices = [ u"Bing", u"Google" ]
        self.s_radioBox2 = wx.RadioBox( self, wx.ID_ANY, _("Use translate services"), wx.DefaultPosition,
                                        wx.Size( 160,-1 ), s_radioBox2Choices, 1, wx.RA_SPECIFY_COLS )
        sbSizerRadioButtons.Add( self.s_radioBox2, 1, wx.ALL|wx.EXPAND, 5 )

        bSizerLeft.Add( sbSizerRadioButtons, 3, wx.EXPAND, 5 )
#

        bSizerChoiceCtrl = wx.BoxSizer( wx.HORIZONTAL )

        sbSizerSearch = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Choose search services") ), wx.HORIZONTAL )

        self.s_choiceSearch = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 150,-1 ),
                                         options.searchEngines, 0 )
        sbSizerSearch.Add( self.s_choiceSearch, 1, wx.ALL|wx.EXPAND, 5 )

        bSizerChoiceCtrl.Add( sbSizerSearch, 0, wx.EXPAND, 5 )

        sbSizerDblCtrl = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _("Use double Control") ), wx.VERTICAL )

        self.s_checkBoxDblCtrl = wx.CheckBox( self, wx.ID_ANY, _("Translate with double CTRL"),
                                              wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizerDblCtrl.Add( self.s_checkBoxDblCtrl, 0, wx.ALL, 5 )

        bSizerChoiceCtrl.Add( sbSizerDblCtrl, 1, wx.EXPAND, 5 )

        bSizerLeft.Add( bSizerChoiceCtrl, 1, wx.EXPAND, 5 )

        bSizerSetting.Add( bSizerLeft, 1, wx.EXPAND, 5 )

        bSizerMain.Add( bSizerSetting, 7, wx.EXPAND, 5 )

        bSizerBottom = wx.BoxSizer( wx.HORIZONTAL )

        bSizerMessage = wx.BoxSizer( wx.HORIZONTAL )

        self.s_staticTextMessage = wx.StaticText( self, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.s_staticTextMessage.Wrap( -1 )
        self.s_staticTextMessage.SetForegroundColour( wx.Colour( 255, 0, 0 ) )

        bSizerMessage.Add( self.s_staticTextMessage, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        bSizerBottom.Add( bSizerMessage, 1, wx.EXPAND, 5 )

        bSizerButtons = wx.BoxSizer( wx.HORIZONTAL )

        self.s_buttonCancel = wx.Button( self, wx.ID_ANY, _("Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerButtons.Add( self.s_buttonCancel, 0, wx.ALIGN_RIGHT|wx.ALL|wx.EXPAND, 5 )

        self.s_buttonSave = wx.Button( self, wx.ID_ANY, _("Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizerButtons.Add( self.s_buttonSave, 0, wx.ALL|wx.BOTTOM, 5 )

        bSizerBottom.Add( bSizerButtons, 0, wx.EXPAND|wx.ALIGN_BOTTOM, 5 )

        bSizerMain.Add( bSizerBottom, 0, wx.EXPAND, 5 )

        self.SetSizer( bSizerMain )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__(self):
        pass

