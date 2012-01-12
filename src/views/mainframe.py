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
import os
from src.modules import options
from src.modules import gettext_windows

class MainTaskBarIcon(wx.TaskBarIcon):

    def __init__(self, parent):
        wx.TaskBarIcon.__init__(self)
        self.parentApp = parent
        if os.name=="posix":
            self.mainIcon = wx.Icon(options.get_main_dir()+"/src/icons/appicons/app_icon_main24.png",wx.BITMAP_TYPE_PNG)
        elif os.name=="nt":
            self.mainIcon = wx.Icon(options.get_main_dir()+"/src/icons/appicons/app_icon.ico",wx.BITMAP_TYPE_ICO)

        self.create_menu()
        self.set_icon_image()

    def create_menu(self):
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.show_menu)
        self.menu=wx.Menu()
        self.menuSetting=wx.MenuItem(self.menu,wx.ID_ANY,_("Settings"))
        self.menuAbout=wx.MenuItem(self.menu,wx.ID_ANY,_("About"))
        self.menuItemDblCtrl = wx.MenuItem( self.menu, wx.ID_ANY, _("Translate with double CTRL") , kind=wx.ITEM_CHECK )
        self.menuItemCtrl = wx.MenuItem( self.menu, wx.ID_ANY, _("With CTRL press") , kind=wx.ITEM_RADIO )
        self.menuItemNothing = wx.MenuItem( self.menu, wx.ID_ANY, _("Nothing press"), kind=wx.ITEM_RADIO )
        self.menuDisableApp = wx.MenuItem( self.menu, wx.ID_ANY, _("Disable Application"), kind=wx.ITEM_RADIO )
        self.menuUseGoogle = wx.MenuItem( self.menu, wx.ID_ANY, "Google", kind=wx.ITEM_RADIO )
        self.menuUseBing = wx.MenuItem( self.menu, wx.ID_ANY, "Bing", kind=wx.ITEM_RADIO )
        self.menu.AppendItem(self.menuItemDblCtrl)
        self.menu.AppendItem(self.menuItemCtrl)
        self.menu.AppendItem(self.menuItemNothing)
        self.menu.AppendItem(self.menuDisableApp)
        self.menu.AppendSeparator()
        self.menu.AppendItem(self.menuUseGoogle)
        self.menu.AppendItem(self.menuUseBing)
        self.menu.AppendSeparator()
        self.menu.AppendItem(self.menuSetting)
        self.menu.AppendItem(self.menuAbout)
        self.menu.AppendSeparator()
        self.menu.Append(wx.ID_EXIT, _('Close'))

    def show_menu(self,event):
        self.PopupMenu(self.menu)

    def set_icon_image(self):
        self.SetIcon(self.mainIcon, "Vertaler")

    def __del__(self):
        pass

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = "Vertaler", pos = wx.DefaultPosition,
                            size = wx.Size( 660,453 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.InitUI()
        self.Centre( wx.BOTH )

    def __del__(self):
        pass

    def InitUI(self):

        self.m_menubar = wx.MenuBar( 0 )
        self.m_menu_file = wx.Menu()
        self.m_menuItemSettings = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _("Settings"),
                                               _("Program settings"), wx.ITEM_NORMAL )
        self.m_menu_file.AppendItem( self.m_menuItemSettings )

        self.m_menu_file.AppendSeparator()

        self.m_menuItemExit = wx.MenuItem( self.m_menu_file, wx.ID_ANY, _("Exit"), _("Close"),
            wx.ITEM_NORMAL )
        self.m_menu_file.AppendItem( self.m_menuItemExit )

        self.m_menubar.Append( self.m_menu_file, _("Main") )

        self.m_menuEdit = wx.Menu()

        self.m_menuItemClear = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _("Clear"),
                                            _("Clear forms"), wx.ITEM_NORMAL )
        self.m_menuEdit.AppendItem( self.m_menuItemClear )

        self.m_menuEdit.AppendSeparator()

        self.m_menuItemCopy = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _("Copy"),
                                           _("Copy text"), wx.ITEM_NORMAL )
        self.m_menuEdit.AppendItem( self.m_menuItemCopy )

        self.m_menuItemPaste = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, _("Paste"),
                                            _("Paste text"), wx.ITEM_NORMAL )
        self.m_menuEdit.AppendItem( self.m_menuItemPaste )

        self.m_menubar.Append( self.m_menuEdit, _("Edit") )

        self.m_menuFastSetting = wx.Menu()
        self.m_menuItemCtrl = wx.MenuItem( self.m_menuFastSetting, wx.ID_ANY, _("With CTRL press"),
                                           _("Translate with CTRL press"), wx.ITEM_RADIO )
        self.m_menuFastSetting.AppendItem( self.m_menuItemCtrl )

        self.m_menuItemNothing = wx.MenuItem( self.m_menuFastSetting, wx.ID_ANY, _("Nothing press"),
                                              _("Translate with nothing press button"), wx.ITEM_RADIO )
        self.m_menuFastSetting.AppendItem( self.m_menuItemNothing )
        self.m_menuItemDisableApp = wx.MenuItem( self.m_menuFastSetting, wx.ID_ANY, _("Disable Application"),
            _("Disable Application"), wx.ITEM_RADIO )
        self.m_menuFastSetting.AppendItem( self.m_menuItemDisableApp )
        self.m_menuFastSetting.AppendSeparator()

        self.m_menuItemGoogle = wx.MenuItem( self.m_menuFastSetting, wx.ID_ANY, "Google",
            _("Disable Application"), wx.ITEM_RADIO )
        self.m_menuFastSetting.AppendItem( self.m_menuItemGoogle )
        self.m_menuItemBing = wx.MenuItem( self.m_menuFastSetting, wx.ID_ANY, "Bing",
            _("Disable Application"), wx.ITEM_RADIO )
        self.m_menuFastSetting.AppendItem( self.m_menuItemBing )

        self.m_menuFastSetting.AppendSeparator()


        if os.name =="nt":
            self.m_menuItemStartUpLoad = wx.MenuItem( self.m_menuFastSetting, wx.ID_ANY, _("Load programm on startup"),
                                                      _("Load programm on startup"), wx.ITEM_CHECK )
            self.m_menuFastSetting.AppendItem( self.m_menuItemStartUpLoad )
            self.m_menuItemStartUpLoad.Check( True )

        self.m_menubar.Append( self.m_menuFastSetting, _("Settings") )

        self.m_menuHelp = wx.Menu()

        self.m_menuItemAbout = wx.MenuItem( self.m_menuHelp, wx.ID_ANY, _("About"), _("About programm"),
                                            wx.ITEM_NORMAL )
        self.m_menuHelp.AppendItem( self.m_menuItemAbout )

        self.m_menubar.Append( self.m_menuHelp, _("Help") )

        self.SetMenuBar( self.m_menubar )

        panel = wx.Panel( self, -1, pos = wx.DefaultPosition, style = wx.TAB_TRAVERSAL )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )

        bSizer = wx.BoxSizer( wx.VERTICAL )

        bSizerFrom = wx.BoxSizer( wx.HORIZONTAL )

        self.m_textCtrlFrom = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                           wx.TE_MULTILINE|wx.TE_NOHIDESEL )
        self.m_textCtrlFrom.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        bSizerFrom.Add( self.m_textCtrlFrom, 1, wx.ALL|wx.EXPAND, 1 )

        bSizer.Add( bSizerFrom, 4, wx.EXPAND, 1 )

        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_bpButtonClear = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/mainframe/edit-clear-2.png",
                                            wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.m_bpButtonClear.SetToolTipString(_("Clear all"))

        bSizer21.Add( self.m_bpButtonClear, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_bpButtonPaste = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/mainframe/edit-paste-2.png",
                                            wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.m_bpButtonPaste.SetToolTipString( _("Paste text from clipboard") )

        bSizer21.Add( self.m_bpButtonPaste, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_bpButtonCopy = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/mainframe/edit-copy-8.png",
                                            wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.m_bpButtonCopy.SetToolTipString( _("Copy translated text") )

        bSizer21.Add( self.m_bpButtonCopy, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.LI_HORIZONTAL|wx.LI_VERTICAL )
        bSizer21.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_bpButtonTranslate = wx.BitmapButton( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/mainframe/view-refresh-3.png",
                                            wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )

        self.m_bpButtonTranslate.SetToolTipString( _("Translate text") )

        bSizer21.Add( self.m_bpButtonTranslate, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticline2 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.LI_HORIZONTAL|wx.LI_VERTICAL )
        bSizer21.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

        m_choiceFromChoices = [ u"Auto", u"English", u"Russian" ]
        self.m_choiceFrom = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choiceFromChoices, 0 )
        self.m_choiceFrom.SetSelection( 0 )
        self.m_choiceFrom.SetToolTipString( _("Translate from") )

        bSizer21.Add( self.m_choiceFrom, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.Bitmap(
            options.get_main_dir()+"/src/icons/mainframe/go-next-3.png",
                                                      wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.m_bitmap1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        m_choiceToChoices = [ u"Russian", u"English" ]
        self.m_choiceTo = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choiceToChoices, 0 )
        self.m_choiceTo.SetSelection( 0 )
        self.m_choiceTo.SetToolTipString( _("Translate to") )

        bSizer21.Add( self.m_choiceTo, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_bpButtonLanguageSetting = wx.BitmapButton( self, wx.ID_ANY,
                    wx.Bitmap(options.get_main_dir()+"/src/icons/mainframe/applications-development-translation.png",
                                           wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.m_bpButtonLanguageSetting.SetToolTipString( _("Open language settings") )

        bSizer21.Add( self.m_bpButtonLanguageSetting, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_bpButtonLanguageSave = wx.BitmapButton( self, wx.ID_ANY,
                                wx.Bitmap( options.get_main_dir()+"/src/icons/mainframe/document-export-2.png",
                                                      wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize,
                                                       wx.BU_AUTODRAW )
        self.m_bpButtonLanguageSave.SetToolTipString( _("Save language settings") )

        bSizer21.Add( self.m_bpButtonLanguageSave, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.LI_HORIZONTAL|wx.LI_VERTICAL )
        bSizer21.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_bpButtonSettings = wx.BitmapButton( self, wx.ID_ANY,
                            wx.Bitmap( options.get_main_dir()+"/src/icons/mainframe/preferences-system-3.png",
                                                      wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize,
                                                   wx.BU_AUTODRAW )
        self.m_bpButtonSettings.SetToolTipString( _("Open settings") )

        bSizer21.Add( self.m_bpButtonSettings, 0, wx.ALIGN_CENTER|wx.ALL, 5 )



        bSizer.Add( bSizer21, 1, wx.EXPAND, 1 )

        bSizerTo = wx.BoxSizer( wx.HORIZONTAL )

        self.m_textCtrlTo = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                         wx.TE_MULTILINE|wx.TE_NOHIDESEL )
        self.m_textCtrlTo.SetFont( wx.Font( 12, 70, 90, 90, False, wx.EmptyString ) )
        bSizerTo.Add( self.m_textCtrlTo, 1, wx.ALL|wx.EXPAND, 1 )

        bSizer.Add( bSizerTo, 4, wx.EXPAND, 1 )

        self.SetSizer( bSizer )
        self.Layout()

        self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )

        favicon = wx.Icon(options.get_main_dir()+"/src/icons/appicons/app_icon.ico", wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(favicon)
#        self.tbicon = MainTaskBarIcon(self)




