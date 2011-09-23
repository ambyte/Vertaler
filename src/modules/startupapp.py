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

""" startup application when start Windows """

import os

if os.name == "nt":
    import winshell
import sys

def is_start_up():
    try:
        startup = winshell.startup(1)
        if os.path.exists(startup + '\\Vertaler.lnk'):
            return True
        else:
            return False
    except Exception:
        pass


def set_startup():
    try:
    #        get path and file name for application
        startFile = os.path.abspath(sys.argv[0])
        #        get startup folder
        startup = winshell.startup(1)
        #        create shortcut in startup folder
        winshell.CreateShortcut(
            Path=os.path.join(startup, "Vertaler.lnk"),
            Target=startFile,
            Icon=(startFile, 0),
            Description="Vertaler",
            StartIn=os.path.abspath(None)
        )
    except Exception:
        pass


def delete_startup():
    try:
        startup = winshell.startup(1)
        #        remove shortcut from startup folder
        if os.path.isfile(startup + '\\Vertaler.lnk'):
            os.remove(startup + '\\Vertaler.lnk')
    except Exception:
        pass




