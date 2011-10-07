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

""" get and set clipboard data"""


import random
import time
import win32api
import win32clipboard
import win32con

def save_clipboard(self):
    cbOpened = False
    while not cbOpened:
        try:
            win32clipboard.OpenClipboard(0)
            cbOpened = True
            self.cbSaved = {}
            rval = win32clipboard.EnumClipboardFormats( 0 )
            while rval:
                #print "Retrieving CB format %d" % rval
#                dat = win32clipboard.GetClipboardData( rval )
                win32clipboard.GetClipboardData( rval )
                if rval == 15:  #CF_HDROP
                    #this'll error, so just give up
                    self.cbSaved = {}
                    win32clipboard.EmptyClipboard()
                    break
                else:
                    self.cbSaved[ rval ] = win32clipboard.GetClipboardData( rval )
                rval = win32clipboard.EnumClipboardFormats( rval )
            win32clipboard.CloseClipboard()
        except Exception, err:
            if err[0] == 5:  #Access Denied
                #print 'waiting on clipboard...'
                time.sleep( random.random()/50 )
                pass
            elif err[0]== 6:
                #print 'clipboard type error, aborting...'
                win32clipboard.CloseClipboard()
                break
            elif err[0] == 1418:  #doesn't have board open
                cbOpened = False
            elif not err[0]:  #open failure
                cbOpened = False
            else:
                pass

# Restore the user's clipboard, if possible
def restore_clipboard(self):
    cbOpened = False

    # don't wait for the CB if we don't have to
    if len(self.cbSaved) > 0:
        #open clipboard
        while not cbOpened:
            try:
                win32clipboard.OpenClipboard(0)
                win32clipboard.EmptyClipboard()
                cbOpened = True
            except Exception, err:
                if err[0] == 5:  #Access Denied
                    #print 'waiting on clipboard...'
                    time.sleep( random.random()/50 )
                    pass
                elif err[0] == 1418:  #doesn't have board open
                    cbOpened = False
                elif not err[0]:  #open failure
                    cbOpened = False
                else:
                    pass
        #replace items
        try:
            for item in self.cbSaved:
                data = self.cbSaved.get(item)
                # windows appends NULL to most clipboard items, so strip off the NULL
                if data[-1] == '\0':
                    data = data[:-1]
                win32clipboard.SetClipboardData( item, data )
        except Exception, err:
            win32clipboard.EmptyClipboard()
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass

def empty_clipboard(self):
    win32clipboard.OpenClipboard(0)
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()
    return True

def event_clipboard(self):
    time.sleep(0.05)
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(ord('C'), 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
    win32api.keybd_event (win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event (ord('C'), 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.05)

def event_press_ctrl():
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event (win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

def run_clipboard(self):
    save_clipboard(self)
    empty_clipboard(self)
    event_clipboard(self)