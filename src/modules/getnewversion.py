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

""" Report if having new version """
import os
import httprequest
import re
from wx.lib.pubsub import Publisher as pub
from threading import Thread
import wx

class NewVersionThread(Thread):
    """Thread Class."""

    def __init__(self,about):
        """Init Worker Thread Class."""
        self.about=about
        Thread.__init__(self)
        self.start()    # start the thread

    def run(self):
        """Run Worker Thread."""
#        url='http://www.vertalerproject.org'
        url3='http://nojsstats.appspot.com/UA-29210353-1/ambyte.github.com/Vertaler/'
        url4='http://www.google-analytics.com/__utm.gif?utmwv=1&utmn=90574207&utmsr=-&utmsc=-&utmul=-&utmje=0&utmfl=-&utmdt=-&utmhn=ambyte.github.com/Vertaler/loadcount.html&utmr=&utmp=&utmac=UA-29210353-1&utmcc=__utma%3D12186020.772354201.1329313389.1329313389.1329313389.1%3B%2B__utmb%3D12186020%3B%2B__utmc%3D12186020%3B%2B__utmz%3D12186020.1329313389.2.2.utmccn%3D(direct)%7Cutmcsr%3D(direct)%7Cutmcmd%3D(none)%3B%2B__utmv%3D12186020.81.26.131.98%3B'
        url2='http://ambyte.github.com/Vertaler/loadcount.html'
        headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11', 'Accept-Charset': 'utf-8' }
        request=httprequest.HttpRequest()
        response=request.http_request(url4,method='GET')
        redg=response
#        result=''
#        try:
#            request=httprequest.HttpRequest()
#            response=request.http_request(url,method='GET')
#            res=re.compile(r'(the new version of program - )(\w+\W\w+)')
#            rv=res.findall(response)
#            result=float(rv[0][1])
#        except Exception, e:
#            result=0
#        finally:
#            if not self.about:
#                wx.CallAfter(pub.sendMessage,"VERSION", result)
#            else:
#                wx.CallAfter(pub.sendMessage,"VERSION ABOUT", result)

    