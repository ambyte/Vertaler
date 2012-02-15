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

""" Controller for MainFrame """
import os
import wx
from src.modules.settings import setandgetsettings, config
from src.modules.translateservices import translatethread

if os.name =="nt":
    from src.modules import startupapp
from wx.lib.pubsub import pub
from src.gui.mainframe import MainFrame, MainTaskBarIcon
from src.controllers import settinglangcontroller , aboutcontroller, settingcontroller
from src.modules import options
from src.modules.settings.config import langForTran


class MainFrameController():

    def __init__(self):
         publisher = pub.Publisher()
         self.view = MainFrame(None)
         self.settings = setandgetsettings.Settings()
         if os.name =="nt":
             if startupapp.is_start_up():
                config.startWithOS=True
                self.view.m_menuItemStartUpLoad.Check(config.startWithOS)
             else:
                config.startWithOS=False
         self.isShow=False
         self.langSetting = settinglangcontroller.SettingLangController()
         self.tbicon = MainTaskBarIcon(self)
         publisher.subscribe(self.set_lang_for_use, "SAVE LANG")
         publisher.subscribe(self.open_text_in_mainframe, "GO HOME")
         publisher.subscribe(self.translate_result, "MAINTRANSLATE")
         publisher.subscribe(self.check_press,"SAVE SETTINGS")
         self.set_lang_for_use(1)
         self.isSaveSetting=False
         self.isMenu=False
         self.isTbicon=False

         self.view.Bind(wx.EVT_CLOSE,self.event_hide)

         self.view.m_menuItemCtrl.Check(config.useControl)
         self.view.m_menuItemNothing.Check(config.useNothing)
         self.view.m_menuItemBing.Check(config.useBing)
         self.view.m_menuItemGoogle.Check(config.useGoogle)

         self.tbicon.menuItemCtrl.Check(config.useControl)
         self.tbicon.menuItemNothing.Check(config.useNothing)
         self.tbicon.menuItemDblCtrl.Check(config.useDblControl)

         self.tbicon.menuUseBing.Check(config.useBing)
         self.tbicon.menuUseGoogle.Check(config.useGoogle)

         # Connect TaskBar Events
         wx.EVT_TASKBAR_LEFT_DCLICK(self.tbicon, self.event_restore_window)
         self.tbicon.Bind( wx.EVT_MENU,self.event_about, self.tbicon.menuAbout  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_settings, self.tbicon.menuSetting  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_check_dbl_ctrl, self.tbicon.menuItemDblCtrl  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_check_press_tbicon, self.tbicon.menuItemCtrl  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_check_press_tbicon, self.tbicon.menuItemNothing  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_check_press_tbicon, self.tbicon.menuDisableApp  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_tbicon_services, self.tbicon.menuUseBing  )
         self.tbicon.Bind( wx.EVT_MENU,self.event_tbicon_services, self.tbicon.menuUseGoogle  )
         self.view.Bind(wx.EVT_ICONIZE, self.event_hide)

         # Connect Menu events

         self.view.Bind( wx.EVT_MENU,self.event_settings, self.view.m_menuItemSettings  )

         self.view.Bind( wx.EVT_MENU,self.event_clear, self.view.m_menuItemClear  )
         self.view.Bind( wx.EVT_MENU,self.event_copy, self.view.m_menuItemCopy  )
         self.view.Bind( wx.EVT_MENU,self.event_paste, self.view.m_menuItemPaste  )

         self.view.Bind( wx.EVT_MENU,self.event_check_press_menu, self.view.m_menuItemCtrl  )
         self.view.Bind( wx.EVT_MENU,self.event_check_press_menu, self.view.m_menuItemNothing  )
         self.view.Bind( wx.EVT_MENU,self.event_check_press_menu, self.view.m_menuItemDisableApp  )
         self.view.Bind( wx.EVT_MENU,self.event_check_press_services, self.view.m_menuItemBing  )
         self.view.Bind( wx.EVT_MENU,self.event_check_press_services, self.view.m_menuItemGoogle  )
         if os.name =="nt":
            self.view.Bind( wx.EVT_MENU,self.event_setting_start_up, self.view.m_menuItemStartUpLoad  )

         self.view.Bind( wx.EVT_MENU,self.event_about, self.view.m_menuItemAbout  )

         # Status bar events

         self.view.m_bpButtonClear.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_bpButtonPaste.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_bpButtonCopy.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_bpButtonTranslate.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_choiceFrom.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_choiceTo.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_bpButtonLanguageSave.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_bpButtonLanguageSetting.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )
         self.view.m_bpButtonSettings.Bind( wx.EVT_ENTER_WINDOW, self.event_mouse_enter )

         self.view.m_bpButtonClear.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_bpButtonPaste.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_bpButtonCopy.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_bpButtonTranslate.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_choiceFrom.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_choiceTo.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_bpButtonLanguageSave.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_bpButtonLanguageSetting.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )
         self.view.m_bpButtonSettings.Bind( wx.EVT_LEAVE_WINDOW, self.event_mouse_leave )

         # Panel events

         self.view.m_bpButtonClear.Bind( wx.EVT_BUTTON, self.event_clear )
         self.view.m_bpButtonPaste.Bind( wx.EVT_BUTTON, self.event_paste )
         self.view.m_bpButtonCopy.Bind( wx.EVT_BUTTON, self.event_copy )

         self.view.m_bpButtonTranslate.Bind( wx.EVT_BUTTON, self.event_translate )

         self.view.m_choiceFrom.Bind( wx.EVT_CHOICE, self.event_choice_from )
         self.view.m_choiceTo.Bind( wx.EVT_CHOICE, self.event_choice_to )
         self.view.m_bpButtonLanguageSave.Bind( wx.EVT_BUTTON, self.event_lang_save )
         self.view.m_bpButtonLanguageSetting.Bind( wx.EVT_BUTTON, self.event_lang_setting )
         self.view.m_bpButtonSettings.Bind( wx.EVT_BUTTON, self.event_settings)

    # Events functions

    def event_hide(self, event):
        """
        application hide into taskbar
        """

        if os.name =="nt":
            self.view.Hide()
            self.clear_text_ctrl()
        else:
            if not self.isShow:
                self.view.Hide()
                self.clear_text_ctrl()
            self.isShow=False


    def event_mouse_enter(self, event):
        """
        get tooltip from button and set tip into statusbar
        """
        self.view.m_statusBar1.SetStatusText(event.EventObject.GetToolTip().Tip)
        event.Skip()

    def event_mouse_leave(self, event):
        """
        get tooltip from button and set tip into statusbar
        """
        self.view.m_statusBar1.SetStatusText('')
        event.Skip()

    def event_restore_window(self,event):
        """
        restore MainFrame when double clicking taskbar icon
        """
        self.isShow=True
        if not self.view.IsShown():
            self.view.Show()
            self.view.Restore()
            self.view.Centre()

    def event_lang_save(self, event):
        """
        Save default languages for translate
        """
        if not len(self.view.m_choiceTo.Items):
            return 0
        item = self.view.m_choiceFrom.GetSelection()
        if not item:
            config.defaultLangFrom='Auto'
        else:
            config.defaultLangFrom= config.langList[item-1]
        item = self.view.m_choiceTo.GetSelection()
        config.defaultLangTo= config.langList[item]
        self.settings.save_lang_param()
        self.view.m_bpButtonLanguageSave.Enable(False)

    def event_clear( self, event ):
        """
        Event for clear textCtrl
        """
        self.clear_text_ctrl()

    def clear_text_ctrl(self):
        """
        Clear textCtrl
        """
        self.view.m_textCtrlFrom.Value = wx.EmptyString
        self.view.m_textCtrlTo.Value = wx.EmptyString

    def event_copy( self, event ):
        """
        Copy translated text
        """
        data = wx.TextDataObject()
        data.SetText(self.view.m_textCtrlTo.Value)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        else:
            wx.MessageBox(_("Unable to open the clipboard"), _("Error"))

    def event_paste( self, event ):
        """
        paste text from clipboard
        """
        success = False
        data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()
        if success:
            self.view.m_textCtrlFrom.SetValue(data.GetText())
        else:
            wx.MessageBox(_("No data in the clipboard in the required format"),_("Error"))

    def event_check_press_menu(self, event):
        """
        translate text when press button
        """
        self.isMenu=True
        if not self.isSaveSetting and not self.isTbicon:
            config.useControl=self.view.m_menuItemCtrl.IsChecked()
            config.useNothing=self.view.m_menuItemNothing.IsChecked()
            config.enableApp=not self.view.m_menuItemDisableApp.IsChecked()
            self.tbicon.menuItemCtrl.Check(config.useControl)
            self.tbicon.menuItemNothing.Check(config.useNothing)
            self.tbicon.menuDisableApp.Check(not config.enableApp)
        self.isMenu=False

    def event_check_dbl_ctrl(self, event):
        config.useDblControl=self.tbicon.menuItemDblCtrl.IsChecked()

    def event_check_press_tbicon(self, event):
        """
        translate text when press button
        """
        self.isTbicon=True
        if not self.isSaveSetting and not self.isMenu:
            config.useControl=self.tbicon.menuItemCtrl.IsChecked()
            config.useNothing=self.tbicon.menuItemNothing.IsChecked()
            config.enableApp=not self.tbicon.menuDisableApp.IsChecked()
            self.view.m_menuItemCtrl.Check(config.useControl)
            self.view.m_menuItemNothing.Check(config.useNothing)
            self.view.m_menuItemDisableApp.Check(not config.enableApp)
        self.isTbicon=False
        self.settings.set_global_params()

    def event_tbicon_services(self,event):
        """
        change translate service
        """
#        TODO проверить работу в Linux
        if self.tbicon.menuUseBing.IsChecked():
            config.useGoogle=False
            config.useBing=True
            self.view.m_menuItemBing.Check(config.useBing)
            self.view.m_menuItemGoogle.Check(config.useGoogle)
        else:
            config.useGoogle=True
            config.useBing=False
            self.view.m_menuItemBing.Check(config.useBing)
            self.view.m_menuItemGoogle.Check(config.useGoogle)


    def event_check_press_services(self,event):
        """
        change translate service
        """
        if self.view.m_menuItemBing.IsChecked():
            config.useGoogle=False
            config.useBing=True
            self.tbicon.menuUseBing.Check(config.useBing)
            self.tbicon.menuUseGoogle.Check(config.useGoogle)
        else:
            config.useGoogle=True
            config.useBing=False
            self.tbicon.menuUseBing.Check(config.useBing)
            self.tbicon.menuUseGoogle.Check(config.useGoogle)

    def check_press(self,msg):
        """
        if change params in setting frame
        """
        self.isSaveSetting=True
        if os.name =="nt":
            self.view.m_menuItemStartUpLoad.Check(config.startWithOS)
        self.view.m_menuItemBing.Check(config.useBing)
        self.view.m_menuItemCtrl.Check(config.useControl)
        self.view.m_menuItemNothing.Check(config.useNothing)
        self.view.m_menuItemGoogle.Check(config.useGoogle)
        self.tbicon.menuItemCtrl.Check(config.useControl)
        self.tbicon.menuItemNothing.Check(config.useNothing)
        self.tbicon.menuItemDblCtrl.Check(config.useDblControl)
        self.tbicon.menuUseBing.Check(config.useBing)
        self.tbicon.menuUseGoogle.Check(config.useGoogle)
        self.isSaveSetting=False

    def event_setting_start_up( self, event ):
        """
        Start application with OS
        """
        config.startWithOS=self.view.m_menuItemStartUpLoad.IsChecked()
        if config.startWithOS:
            startupapp.set_startup()
        else:
            startupapp.delete_startup()


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

    def event_lang_setting( self, event ):
        """
        Open language SettingFrame
        """
        self.langSetting.view.ShowModal()

    def event_choice_from( self, event ):
        """
        Enable button LanguageSave
        """
        if self.view.m_choiceFrom.GetStringSelection()=="--------":
            self.view.m_choiceFrom.SetSelection(self.view.m_choiceFrom.Selection-1)
        self.view.m_bpButtonLanguageSave.Enable(True)

    def event_choice_to( self, event ):
        """
        Enable button LanguageSave
        """
        if self.view.m_choiceTo.GetStringSelection()=="--------":
            self.view.m_choiceTo.SetSelection(self.view.m_choiceTo.Selection-1)
        self.view.m_bpButtonLanguageSave.Enable(True)

    def event_translate( self, event ):
        """
        Translate text
        """
        if self.view.m_textCtrlFrom.Value != "":
            self.view.m_textCtrlTo.SetValue("")
            langFrom=self.languagesFrom[self.view.m_choiceFrom.Selection]
            langTo=self.languagesTo[self.view.m_choiceTo.Selection]
            _targetLang=''
            _sourceLang=''
            for k, v in langForTran.iteritems():
                if v==langTo:
                    _targetLang=k
                if v==langFrom:
                    _sourceLang=k
            if langFrom=='Auto':
                _sourceLang="auto"
            self.view.m_bpButtonTranslate.Enable(False)
            translatethread.TranslateThread(self.view.m_textCtrlFrom.Value,sourceLang=_sourceLang,
                                            targetLang=_targetLang, mainTranslate=1,view=self.view.m_textCtrlTo)
        else:
            dial = wx.MessageDialog(None, _('Inter text'), _('Error'), wx.OK |  wx.ICON_ERROR)
            dial.ShowModal()

    def set_lang_for_use(self,msg):
        """
        When save languages SettingFrame filling m_choiceFrom and m_choiceTo
        """
        self.languagesFrom=[]
        self.languagesTo=[]
        languages=[]
        for k, v in langForTran.iteritems():
            languages.append(v)
        countItem=0
        languages.sort()
        languagesCopy=list(languages)
        for s in languagesCopy:
            if s in config.langList:
                languages.remove(s)
                languages.insert(countItem,s)
                countItem+=1
            if countItem == len(config.langList):
                languages.insert(countItem,"--------")
                break

        self.languagesTo=languages
        self.languagesFrom=['Auto']+languages
        self.view.m_choiceFrom.SetItems(self.languagesFrom)
        if config.defaultLangFrom:
            self.view.m_choiceFrom.Selection=self.languagesFrom.index(config.defaultLangFrom)
        self.view.m_choiceTo.SetItems(self.languagesTo)
        if config.defaultLangTo:
            self.view.m_choiceTo.Selection = self.languagesTo.index(config.defaultLangTo)

    def translate_result(self, msg):
        """
        Receives data from thread and updates the display
        """
        self.view.m_bpButtonTranslate.Enable(True)
        lang=''
        if self.view.m_choiceFrom.GetStringSelection() == 'Auto':
            for k, v in langForTran.iteritems():
                    if k==msg.data[0]:
                        lang=v
            self.view.m_textCtrlTo.SetValue(msg.data[1]+'\n('+_('Source lang is ') +lang+')')
        else: self.view.m_textCtrlTo.SetValue(msg.data[1])

    def open_text_in_mainframe(self, arg):
        """
        Open text from PopUpFrame in MainFrame
        """
        self.isShow=True
        self.view.m_textCtrlFrom.SetValue(arg.data)
        self.view.Show(True)


