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

""" Thread for translate text """
import os

import wx
import time

from threading import Thread
from wx.lib.pubsub import pub
from src.modules.settings.config import langForTran
from src.modules.settings import config
from src.modules.translateservices.translatebing import Translator
from src.modules.translateservices.translategoogle import translate_google

class TranslateThread(Thread):
    """Thread Class."""

    def __init__(self, sourceText,sourceLang="auto", targetLang="ru", mainTranslate=0, view=None,countRunTranslator=0):
        """Init Worker Thread Class."""
        self.mainTranslate = mainTranslate
        self.sourceText=sourceText
        self.sourceLang=sourceLang
        self.targetLang=targetLang
        self.countRunTranslator=countRunTranslator
        self.view=view
        Thread.__init__(self)
        self.start()    # start the thread

    def run(self):
        """Run Worker Thread."""
#        options.isRunTranslate=False
        publisher = pub.Publisher()
        result=[]
        try:
            if self.sourceLang=="auto": self.sourceLang=None
            tran= Translator('5879888D232D8A18B987C92997518E37EEEF20AB')
            sourceL=tran.detect(self.sourceText.encode("utf-8"))
#            sourceL=tran.detect(self.sourceText)
            # if language of source text is target language then target language equally source language
            if self.targetLang==sourceL and len(config.langList)==2:
                for lang in config.langList:
                    langAbr=''
                    for k, v in langForTran.iteritems():
                        if v==lang:
                            langAbr=k
                    if langAbr!=self.targetLang:
                        self.targetLang=langAbr
                        break
            time.sleep(0.1)
            result.append(sourceL)
            if config.useBing:
                result.append(tran.translate(self.sourceText.encode("utf-8"),self.targetLang,from_lang=self.sourceLang))
            if config.useGoogle:
                if os.name=="nt":
                    result.append(translate_google(self.sourceText,self.sourceLang,self.targetLang))
                else:
                    result.append(translate_google(self.sourceText.decode("utf-8"),self.sourceLang,self.targetLang))
            result.append(self.countRunTranslator)
#            print result[1]
            time.sleep(0.1)
            if not self.mainTranslate:
                wx.CallAfter(publisher.sendMessage,"TRANSLATE", result)
            else:
                wx.CallAfter(publisher.sendMessage,"MAINTRANSLATE", result)
        except Exception:
            result=("",self.countRunTranslator,"Sorry, an error occurred")
            if not self.mainTranslate:
                wx.CallAfter(publisher.sendMessage,"TRANSLATE", result)
            else:
                wx.CallAfter(publisher.sendMessage,"MAINTRANSLATE", result)