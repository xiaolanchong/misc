#!/usr/bin/python3.2
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eugeneg
#
# Created:     18/09/2012
# Copyright:   (c) eugeneg 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import datetime
import sys
import os.path
import win32gui
import win32process
import win32api
import win32con
import tkinter as tk

from Activity import getActivity

############################################################################
class ActivityLogger:
    def __init__(self):
        self.file = open('activity.txt', mode= 'a', buffering=1, encoding='utf-8')

    def AddNewActivity(self, appName, extraInfo, start, end):
        duration = end - start
        s = '{0:.1f}, {1}, {2}, {3}, {4}'.format(duration.total_seconds() / 60,
               start.strftime('%Y-%m-%d %H:%M'), end.strftime('%Y-%m-%d %H:%M'),
               appName, extraInfo)
        self.file.write(s + '\n')

############################################################################
class App():
    def __init__(self):
        self.root = tk.Tk()
        self.label = tk.Label(text="")
        self.label.pack()
        self.activityLogger = ActivityLogger()
        exename, caption = getCurrentProcessName()
        self.currentActivity = getActivity(exename, caption)
        self.update_clock()
        self.root.protocol("WM_DELETE_WINDOW", self.onClose)
        self.root.withdraw()
        self.root.mainloop()

    def update_clock(self):
        self.oneCycle()
        self.root.after(10000, self.update_clock)

    def oneCycle(self):
        idle = not self.isUserActive()
        exename, caption = getCurrentProcessName()
        if exename and caption:
            self.currentActivity = self.currentActivity.OnTimer(idle, exename,
                        caption, self.activityLogger)
        else:
            print('Failed to get wnd')

    def onClose(self):
        self.currentActivity.Close(self.activityLogger)
        self.root.destroy()

    def isUserActive(self):
        idleTime = win32api.GetTickCount() - win32api.GetLastInputInfo()
        return (idleTime / 1000) < 60


############################################################################
def getCurrentProcessName():
    pshandle = None
    try:

        isVistaAndLater = sys.getwindowsversion().major >= 6
        curWnd = win32gui.GetForegroundWindow()
        processid = win32process.GetWindowThreadProcessId(curWnd)
        pshandle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION
                        | win32con.PROCESS_VM_READ, False, processid[1])
        if isVistaAndLater:
            import ctypes
            import ctypes.wintypes as wintypes
            MAX_PATH = 260
            applicationPath = ctypes.create_unicode_buffer(MAX_PATH)
            length = wintypes.DWORD(MAX_PATH)
            handle = wintypes.HANDLE(int(pshandle))
            kernel32 = ctypes.windll.kernel32
            kernel32.QueryFullProcessImageNameW(handle, 0, applicationPath, ctypes.byref(length))
            exename = applicationPath.value
        else:
            exename = win32process.GetModuleFileNameEx(pshandle, 0)
    except Exception as e:
      #  print(e)
        return (None, None)
    finally:
        win32api.CloseHandle(pshandle)
    caption = win32gui.GetWindowText(curWnd)
    fileName = os.path.basename(exename).split('.')[0]
    return (fileName, caption)

################################################################################
def main():
    app=App()


if __name__ == '__main__':
    main()
