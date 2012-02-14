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

""" A translator using the micrsoft translation engine """

#from src.packages import requests
import json
from src.modules import gettext_windows, httprequest

class Translator(object):
    """Implements AJAX API for the Microsoft Translator service

    :param app_id: A string containing the Bing AppID.
    """

    def __init__(self, app_id):
        """
        :param app_id: A string containing the Bing AppID.
        """
        self.app_id = app_id

    def call(self, url, params):
        """Calls the given url with the params urlencoded """
        try:
            params['appId'] = self.app_id
            request=httprequest.HttpRequest()
            response=request.http_request(url,params=params,method='GET')
            rv =  json.loads(response.decode("UTF-8-sig"))
            return rv
        except Exception:
            return _("Sorry, Can't connect to the server!")



    def translate(self, text, to_lang, from_lang=None,
            content_type='text/plain', category='general'):
        """Translates a text string from one language to another.

        :param text: A string representing the text to translate.
        :param to_lang: A string representing the language modules to
            translate the text into.
        :param from_lang: A string representing the language modules of the
            translation text. If left None the response will include the
            result of language auto-detection. (Default: None)
        :param content_type: The format of the text being translated.
            The supported formats are "text/plain" and "text/html". Any HTML
            needs to be well-formed.
        :param category: The category of the text to translate. The only
            supported category is "general".
        """
        params = {
            'text': text,
            'to': to_lang,
            'contentType': content_type,
            'category': category,
            }
        if from_lang is not None:
            params['from'] = from_lang
        return self.call(
            "http://api.microsofttranslator.com/V2/Ajax.svc/Translate",
            params)

    def detect( self, text ):
        """
        The Detect method will detect the language modules of a given piece of text
        :param text: text for detecting the language modules.
        """
        params = {'text': text}
        return self.call(
                "http://api.microsofttranslator.com/V2/Ajax.svc/Detect",
                params)





