# -*- coding: utf-8 -*-
version=0.2
visitedVersion=0.2
enableNotification=True
isFirstStart=True
countClickUp=0
langList=['English','Russian']
searchEngines=['Google','Bing','Yahoo','Yandex']
defaultSearchEngine=0
defaultLangFrom='Auto'
defaultLangTo='Russian'
useControl=True
useDblControl=True
useNothing=False
useGoogle=True
useBing=False
useProxy=False
enableApp=True
startWithOS=True
proxyAddress=""
proxyPort=""
proxyLogin=""
proxyPassword=""
isRunTranslate=False
translatedTextSize=8
langForTran = {
'ar':'Arabic',
'bg':'Bulgarian',
'ca':'Catalan',
'zh-CHS':'Chinese Simplified',
'zh-CHT':'Chinese Traditional',
'cs':'Czech',
'da':'Danish',
'nl':'Dutch',
'en':'English',
'et':'Estonian',
'fi':'Finnish',
'fr':'French',
'de':'German',
'el':'Greek',
'ht':'Haitian Creole',
'he':'Hebrew',
'hu':'Hungarian',
'id':'Indonesian',
'it':'Italian',
'ja':'Japanese',
'ko':'Korean',
'lv':'Latvian',
'lt':'Lithuanian',
'no':'Norwegian',
'pl':'Polish',
'pt':'Portuguese',
'ro':'Romanian',
'ru':'Russian',
'sk':'Slovak',
'sl':'Slovenian',
'es':'Spanish',
'sv':'Swedish',
'th':'Thai',
'tr':'Turkish',
'uk':'Ukrainian',
'vi':'Vietnamese'
}

langForListen = {
'ca':'Catalan',
'ca-es':' Catalan (Spain)',
'da':'Danish',
'da-dk':'Danish (Denmark)',
'de':'German',
'de-de':'German (Germany)',
'en':'English',
'en-au':'English (Australia)',
'en-ca':'English (Canada)',
'en-gb':'English (United Kingdom)',
'en-in':'English (India)',
'en-us':'English (United States)',
'es':'Spanish',
'es-es':'Spanish (Spain)',
'es-mx':'Spanish (Mexico)',
'fi   ':'Finnish',
'fi-fi':'Finnish (Finland)',
'fr   ':'French',
'fr-ca':'French (Canada)',
'fr-fr':'French (France)',
'it   ':'Italian',
'it-it':'Italian (Italy)',
'ja   ':'Japanese',
'ja-jp':'Japanese (Japan)',
'ko   ':'Korean',
'ko-kr':'Korean (Korea)',
'nb-no':'Norwegian (Norway)',
'nl':'Dutch',
'nl-nl':'Dutch (Netherlands)',
'no':'Norwegian',
'pl':'Polish',
'pl-pl':'Polish (Poland)',
'pt':'Portuguese',
'pt-br':'Portuguese (Brazil)',
'pt-pt':'Portuguese (Portugal)',
'ru':'Russian',
'ru-ru':'Russian (Russia)',
'sv':'Swedish',
'sv-se':'Swedish (Sweden)',
'zh-chs':'Chinese Simplified',
'zh-cht':'Chinese Traditional',
'zh-hk':'Chinese Traditional (Hong Kong S.A.R.)',
'zh-tw':'Chinese Traditional (Taiwan)'
}

import imp
import os
import sys

def main_is_frozen():
   return (hasattr(sys, "frozen") or # new py2exe
           hasattr(sys, "importers") # old py2exe
           or imp.is_frozen("__main__")) # tools/freeze

def get_main_dir():
   if main_is_frozen():
       # print 'Running from path', os.path.dirname(sys.executable)
       return os.path.dirname(sys.executable)
   return os.path.dirname(sys.argv[0])


  