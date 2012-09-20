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

import datetime

class AppWork():
    def __init__(self, appName, title):
        self.appName = appName
        self.startTime = datetime.datetime.now()
        self.titles = set()
        self.titles.add(title)

    def OnTimer(self, idle, appName, title, activityAccumulator):
        if idle or appName != self.appName:

            self.Close(activityAccumulator)
            return IdleAction() if idle else getActivity(appName, title)
        else:
            self.titles.add(title)
            return self

    def Close(self, activityAccumulator):
            titles = '| '.join(self.titles)
            activityAccumulator.AddNewActivity(self.appName, titles, self.startTime,
                            datetime.datetime.now())

###############################################################################
class IdleAction():
    def __init__(self):
        self.startTime = datetime.datetime.now()

    def OnTimer(self, idle, appName, title, activityAccumulator):
        if not idle:
            self.Close(activityAccumulator)
            assert(len(appName))
            return getActivity(appName, title)
        else:
            return self

    def Close(self, activityAccumulator):
         activityAccumulator.AddNewActivity('<away>', '', self.startTime,
                            datetime.datetime.now())

def getActivity(appName, title):
    assert(len(appName) and appName[-3] != 'exe')
    return AppWork(appName, title)


def main():
    pass

if __name__ == '__main__':
    main()
