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

""" Controller for SettingLang frame """

import wx
from src.modules.settings import options
from src.views.settinglangframe import SettingLangFrame
from wx.lib.pubsub import pub

class SettingLangController:

    def __init__(self):
        self.checkedListChoicesData = options.langList
        self.view = SettingLangFrame(None)

        # Connect Events

        self.view.Bind(wx.EVT_SHOW, self.event_show)
        self.view.l_searchCtrl.Bind( wx.EVT_SEARCHCTRL_CANCEL_BTN, self.event_clear )
        self.view.l_searchCtrl.Bind( wx.EVT_SEARCHCTRL_SEARCH_BTN, self.event_search )
        self.view.l_searchCtrl.Bind( wx.EVT_TEXT, self.event_search )
        self.view.l_searchCtrl.Bind( wx.EVT_TEXT_ENTER, self.event_search )
        self.view.l_checkList.Bind( wx.EVT_CHECKLISTBOX, self.event_check )
        self.view.l_buttonSave.Bind( wx.EVT_BUTTON, self.event_save )
        self.view.l_buttonCancel.Bind( wx.EVT_BUTTON, self.event_cancel )

    # event handlers

    def event_show( self, event ):
        """
        open dialog and set languages in l_checkList
        """
        self.array_lang()

    def event_clear( self, event ):
        """
        clear value in l_searchCtrl
        """
        self.view.l_searchCtrl.Value=wx.EmptyString

    def event_search( self, event ):
        """
        search language
        """
        self.search_lang()

    def event_check( self, event ):
        """
        when check language, add it on up of l_checkList
        """
        for s in self.view.l_checkList.GetCheckedStrings():
            if not s in self.checkedListChoicesData:
                self.checkedListChoicesData.append(s)
        for st in self.view.l_checkList.GetStrings():
            if not st in self.view.l_checkList.GetCheckedStrings() and st in self.checkedListChoicesData:
                self.checkedListChoicesData.remove(st)
        self.checkedListChoicesData.sort()

    def event_save( self, event ):
        """
        save selected languages in options and send message to mainframe
        """
        publisher = pub.Publisher()
        options.langList=self.checkedListChoicesData
        options.langList.sort()
        publisher.sendMessage("SAVE LANG")
        self.view.Close()


    def event_cancel( self, event ):
        """
        close dialog
        """
        self.view.Close()

    def array_lang(self):
        """
        set selected languages
        """
        listChoices = []
        for k, v in options.langForTran.iteritems():
            listChoices.append(v)
        listChoices.sort()
        self.set_list_into_control(listChoices)

    def search_lang(self):
        """
        search language
        """
        listChoices = []
        for k, v in options.langForTran.iteritems():
            if self.view.l_searchCtrl.Value.lower() in v.lower():
                listChoices.append(v)
        listChoices.sort()
        self.set_list_into_control(listChoices)

    def set_list_into_control(self,listChoices):
        """
        set languages in l_checkList
        """
        countItem=0
        checkedListChoicesCopy=list(self.checkedListChoicesData)
        for s in checkedListChoicesCopy:
            if s in listChoices:
                listChoices.remove(s)
                listChoices.insert(countItem,s)
                countItem+=1
        self.view.l_checkList.Set(listChoices)
        listChoicesIn = list(set(listChoices) & set(self.checkedListChoicesData))
        self.view.l_checkList.SetCheckedStrings(listChoicesIn)