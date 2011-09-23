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

import requests
from src.modules import options

class HttpRequest():
    def __init__(self):
        if options.useProxy:
            proxy = options.proxyAddress+":"+options.proxyPort
            user = options.proxyLogin
            password = options.proxyPassword
            self.proxies={'proxy':proxy,'user':user,'password':password}
        else:
            self.proxies=None

    def http_request(self,url,method='POST',params=None,data=None,headers=None):
        response = requests.request(method,url,params=params,data=data,headers=headers,timeout=5,proxies=self.proxies)
        return response.content