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
import wx.xrc
import wx.wizard
from src.modules.settings import config

class PreconfiguringFrame ( wx.wizard.Wizard ):

    def __init__( self ):
        wx.wizard.Wizard.__init__ ( self, None, id = wx.ID_ANY, title = u"Preconfiguring Vertaler",  bitmap = wx.Bitmap( config.get_main_dir()+"/src/icons/appicons/app_image.png", wx.BITMAP_TYPE_ANY ), pos = wx.DefaultPosition, style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.m_pages = []

        self.p_wizPageNatLang = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.p_wizPageNatLang )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.p_staticTextNatLang = wx.StaticText( self.p_wizPageNatLang, wx.ID_ANY, u"Select your native language", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.p_staticTextNatLang.Wrap( -1 )
        self.p_staticTextNatLang.SetFont( wx.Font( 12, 74, 90, 92, False, "Tahoma" ) )

        bSizer3.Add( self.p_staticTextNatLang, 0, wx.ALL|wx.EXPAND, 5 )

        p_listBoxNatLangChoices = []
        self.p_listBoxNatLang = wx.ListBox( self.p_wizPageNatLang, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, p_listBoxNatLangChoices, wx.LB_HSCROLL|wx.LB_SINGLE|wx.LB_SORT )
        self.p_listBoxNatLang.SetFont( wx.Font( 12, 74, 90, 90, False, "Tahoma" ) )

        bSizer3.Add( self.p_listBoxNatLang, 1, wx.ALL|wx.EXPAND, 5 )

        self.p_wizPageNatLang.SetSizer( bSizer3 )
        self.p_wizPageNatLang.Layout()
        bSizer3.Fit( self.p_wizPageNatLang )
        self.p_wizPageComTran = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.p_wizPageComTran )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.p_staticTextComTran = wx.StaticText( self.p_wizPageComTran, wx.ID_ANY, u"Select languages from which most commonly translate", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.p_staticTextComTran.Wrap( -1 )
        self.p_staticTextComTran.SetFont( wx.Font( 12, 74, 90, 92, False, "Tahoma" ) )

        bSizer4.Add( self.p_staticTextComTran, 1, wx.ALL|wx.EXPAND, 5 )

        p_listBoxComTranChoices = []
        self.p_listBoxComTran = wx.ListBox( self.p_wizPageComTran, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, p_listBoxComTranChoices, wx.LB_HSCROLL|wx.LB_MULTIPLE|wx.LB_SORT )
        self.p_listBoxComTran.SetFont( wx.Font( 12, 74, 90, 90, False, "Tahoma" ) )

        bSizer4.Add( self.p_listBoxComTran, 4, wx.ALL|wx.EXPAND, 5 )

        self.p_wizPageComTran.SetSizer( bSizer4 )
        self.p_wizPageComTran.Layout()
        bSizer4.Fit( self.p_wizPageComTran )
        self.p_wizPageOther = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.p_wizPageOther )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        sbSizerSizeText = wx.StaticBoxSizer( wx.StaticBox( self.p_wizPageOther, wx.ID_ANY, u"The size of the text in the translation window" ), wx.VERTICAL )

        self.p_staticTextSizeText = wx.StaticText( self.p_wizPageOther, wx.ID_ANY, u"Translated text", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
        self.p_staticTextSizeText.Wrap( -1 )
        self.p_staticTextSizeText.SetFont( wx.Font( 8, wx.SWISS, wx.NORMAL, wx.NORMAL ) )
        sbSizerSizeText.Add( self.p_staticTextSizeText, 1, wx.ALL, 5 )


        self.p_sliderSizeText = wx.Slider( self.p_wizPageOther, wx.ID_ANY, 0, 0, 10, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )

        sbSizerSizeText.Add( self.p_sliderSizeText, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer5.Add( sbSizerSizeText, 1, wx.EXPAND, 5 )

        sbSizerTranServ = wx.StaticBoxSizer( wx.StaticBox( self.p_wizPageOther, wx.ID_ANY, u"The default translation service" ), wx.VERTICAL )

        self.p_radioBtnGoogle = wx.RadioButton( self.p_wizPageOther, wx.ID_ANY, u"Google", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_radioBtnGoogle.SetValue( True )
        sbSizerTranServ.Add( self.p_radioBtnGoogle, 1, wx.ALL, 5 )

        self.p_radioBtnBing = wx.RadioButton( self.p_wizPageOther, wx.ID_ANY, u"Bing", wx.DefaultPosition, wx.DefaultSize, 0 )
        sbSizerTranServ.Add( self.p_radioBtnBing, 1, wx.ALL, 5 )

        bSizer5.Add( sbSizerTranServ, 1, wx.EXPAND, 5 )

        sbSizerProxy = wx.StaticBoxSizer( wx.StaticBox( self.p_wizPageOther, wx.ID_ANY, u"Proxy server if there is" ), wx.VERTICAL )

        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        self.p_textCtrlAddress = wx.TextCtrl( self.p_wizPageOther, wx.ID_ANY, u"Address", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_textCtrlAddress.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.p_textCtrlAddress.SetToolTipString( u"Address" )
        self.p_textCtrlAddress.Name="0Address"


        bSizer11.Add( self.p_textCtrlAddress, 1, wx.ALL|wx.EXPAND, 5 )

        self.p_textCtrlPort = wx.TextCtrl( self.p_wizPageOther, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_textCtrlPort.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.p_textCtrlPort.SetToolTipString( u"Port" )
        self.p_textCtrlPort.Name="0Port"


        bSizer11.Add( self.p_textCtrlPort, 1, wx.ALL|wx.EXPAND, 5 )

        sbSizerProxy.Add( bSizer11, 1, wx.EXPAND, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.p_textCtrlLogin = wx.TextCtrl( self.p_wizPageOther, wx.ID_ANY, u"Login", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_textCtrlLogin.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.p_textCtrlLogin.SetToolTipString( u"Login" )
        self.p_textCtrlLogin.Name="0Login"


        bSizer12.Add( self.p_textCtrlLogin, 1, wx.ALL|wx.EXPAND, 5 )

        self.p_textCtrlPass = wx.TextCtrl( self.p_wizPageOther, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.p_textCtrlPass.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.p_textCtrlPass.SetToolTipString( u"Password" )
        self.p_textCtrlPass.Name="0Password"


        bSizer12.Add( self.p_textCtrlPass, 1, wx.ALL|wx.EXPAND, 5 )

        sbSizerProxy.Add( bSizer12, 1, wx.EXPAND, 5 )

        bSizer5.Add( sbSizerProxy, 1, wx.EXPAND, 5 )

        self.p_wizPageOther.SetSizer( bSizer5 )
        self.p_wizPageOther.Layout()
        bSizer5.Fit( self.p_wizPageOther )
        self.Centre( wx.BOTH )



    def add_page(self, page):
        if self.m_pages:
            previous_page = self.m_pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.m_pages.append(page)

    def __del__( self ):
        pass












