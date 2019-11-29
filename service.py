from resources.lib.toollib import *
from resources.lib.connection import Connection

class Player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.__isPlaying = False

    def onPlayBackPaused(self):
        self.__isPlaying = False

    def onPlayBackResumed(self):
        self.__isPlaying = True

    def onPlayBackEnded(self):
        self.__isPlaying = False

    def onPlayBackStarted(self):
        self.__isPlaying = True

    def onPlayBackStopped(self):
        self.__isPlaying = False


class Monitor(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.__screenSaverActive = False
        self.__settingsChanged = False

    def onScreensaverActivated(self):
        self.__screenSaverActive = True

    def onScreensaverDeactivated(self):
        self.__screenSaverActive = False

    def onSettingsChanged(self):
        self.__settingsChanged = True


class Hyperion(object):
    def __init__(self):
        self.playr = Player()
        self.monitor = Monitor()
        self.connection = Connection()

        self.getSettings()
        self.start()

    def getSettings(self):
        self.ip = KodiLib().getAddonSetting('ip')
        self.port = KodiLib().getAddonSetting('port')
        self.enableHyperion = KodiLib().getAddonSetting('enableHyperion', sType=BOOL)
        self.disableHyperion = KodiLib().getAddonSetting('disableHyperion', sType=BOOL)
        self.authToken = KodiLib().getAddonSetting('authToken')

        self.opt_videoMode = KodiLib().getAddonSetting('videoMode')
        self.detection_3d = KodiLib().getAddonSetting('detection_3d')
        self.opt_audioMode = KodiLib().getAddonSetting('audioMode')
        self.opt_pauseMode = KodiLib().getAddonSetting('pauseMode')
        self.opt_menuMode = KodiLib().getAddonSetting('menuMode')
        self.opt_screenSaverMode = KodiLib().getAddonSetting('screenSaverMode')

        KodiLib().writeLog('Host')
        KodiLib().writeLog('Enable Hyperion on Start')
        KodiLib().writeLog('Disable Hyperion on Stop')
        

    def start(self):
        pass