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


import re
import httprequest
import json

def translate_google(text, sourcelang="auto", targetlang="ru"):
    url = "http://www.google.com/translate_a/t?client=t"
    headers={ 'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8' }
    data = {'q' : text.encode("UTF-8"),
            'sl': sourcelang,
            'tl': targetlang,
            'ie':'utf-8',
            'oe':'utf-8'
    }

    try:
        request=httprequest.HttpRequest()
        response=request.http_request(url,data=data,headers=headers)
        fixedJSON = re.sub(r',{2,}', ',', response).replace(',]', ']')
        data = json.loads(fixedJSON)
        resultData=''
        try:
            # if many words
            if len(text.split(' '))>1:
                for row in data[2]:
                    resultData+=row[0]+" "
            else:
                resultData=data[0][0][0]
                if not type(data[1]) is unicode:
                    resultData += '\n----\n'
                    for row in data[1][0][1]:
                        if data[1][0][1][len(data[1][0][1])-1] == row:
                            resultData +=u"%s " % row
                        else:
                            resultData +=u"%s " % row
        except Exception:
            pass
        return resultData
    except Exception, e:
        return _("Sorry, Can't connect to the server!")

