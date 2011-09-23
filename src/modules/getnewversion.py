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
        url='http://www.vertalerproject.org'
        result=''
        try:
            request=httprequest.HttpRequest()
            response=request.http_request(url,method='GET')
            res=re.compile(r'(the new version of program - )(\w+\W\w+)')
            rv=res.findall(response)
            result=float(rv[0][1])
        except Exception, e:
            result=0
        finally:
            if not self.about:
                wx.CallAfter(pub.sendMessage,"VERSION", result)
            else:
                wx.CallAfter(pub.sendMessage,"VERSION ABOUT", result)

    