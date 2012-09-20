#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eugeneg
#
# Created:     19/09/2012
# Copyright:   (c) eugeneg 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import datetime
import win32api
from pyhook import HookManager

class UserPresence:
    def isUserActive(self):
        idleTime = win32api.GetTickCount() - win32api.GetLastInputInfo()
        return (idleTime / 1000) < 60


    """
    def __init__(self):
        # create the hook mananger
        self.hm = HookManager()
        # register two callbacks
        self.hm.MouseAllButtonsDown = self.onMouseEvent
        self.hm.KeyDown = self.onKeyboardEvent

        # hook into the mouse and keyboard events
        self.hm.HookMouse()
        self.hm.HookKeyboard()
        self.lastUserActionTime = datetime.datetime.now() # None

    def onMouseEvent(self, *event):
        self.lastUserActionTime = datetime.datetime.now()
        return True

    def onKeyboardEvent(self, *event):
        self.lastUserActionTime = datetime.datetime.now()
        return True

    def isUserActive(self):
        if self.lastUserActionTime is None:
            return False
        else:
            return datetime.datetime.now() < (self.lastUserActionTime + datetime.timedelta(seconds=60))

    """

def main():
    z = UserPresence();
    print(z.isUserActive())
    pass

if __name__ == '__main__':
    main()
