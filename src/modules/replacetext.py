import os
import win32api
import win32clipboard
import time
import win32con
import win32ui
from threading import Thread
import wx
from src.modules import clipboardlib

class ReplaceText(Thread):
    """Thread Class."""
    def __init__(self,text):
        self.translatedText=text
        Thread.__init__(self)
        self.start()    # start the thread

    def run(self):
        try:
#            text=win32con.EM_GETSEL
#            wnd = win32ui.GetForegroundWindow()
#            print wnd.GetWindowText()
            if os.name =="nt":
                if '----' in self.translatedText:
                    count=self.translatedText.find("----")
                    self.translatedText=self.translatedText[:count-len(self.translatedText)]
                clipboardlib.save_clipboard(self)
                clipboardlib.empty_clipboard(self)
                data = wx.TextDataObject()
                data.SetText(self.translatedText)
                if wx.TheClipboard.Open():
                    wx.TheClipboard.SetData(data)
                    wx.TheClipboard.Close()
                    time.sleep(0.05)
                    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                    win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_EXTENDEDKEY | 0, 0)
                    win32api.keybd_event (win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                    win32api.keybd_event (ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
                    time.sleep(0.05)
                clipboardlib.restore_clipboard(self)
        except Exception, err:
            print err.message
#            pass