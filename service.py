from resources.lib.toollib import *
from resources.lib.connection import Connection

EXT = '.png'

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
        self.screenSaverActive = False
        self.settingsChanged = False

    def onScreensaverActivated(self):
        self.screenSaverActive = True

    def onScreensaverDeactivated(self):
        self.screenSaverActive = False

    def onSettingsChanged(self):
        self.settingsChanged = True


class Hyperion(object):
    def __init__(self):
        self.player = Player()
        self.monitor = Monitor()
        self.kl = KodiLib()
        self.stereomode = None

        xbmcgui.Window(10000).setProperty('moodcolor_1', self.kl.getAddonSetting('moodcolor_1'))
        xbmcgui.Window(10000).setProperty('moodcolor_2', self.kl.getAddonSetting('moodcolor_2'))
        xbmcgui.Window(10000).setProperty('moodcolor_3', self.kl.getAddonSetting('moodcolor_3'))

        self.getSettings()
        self.checkColors()
        self.start()

    def checkColors(self):
        if xbmcgui.Window(10000).getProperty('moodcolor_1') != self.moodcolor_1:
            ADDON.setSetting('moodcolor_1', xbmcgui.Window(10000).getProperty('moodcolor_1'))
        if xbmcgui.Window(10000).getProperty('moodcolor_2') != self.moodcolor_2:
            ADDON.setSetting('moodcolor_2', xbmcgui.Window(10000).getProperty('moodcolor_2'))
        if xbmcgui.Window(10000).getProperty('moodcolor_3') != self.moodcolor_3:
            ADDON.setSetting('moodcolor_3', xbmcgui.Window(10000).getProperty('moodcolor_3'))


    def getSettings(self):
        self.ip = self.kl.getAddonSetting('ip')
        self.port = self.kl.getAddonSetting('port')
        self.enableHyperion = self.kl.getAddonSetting('enableHyperion', sType=BOOL)
        self.disableHyperion = self.kl.getAddonSetting('disableHyperion', sType=BOOL)
        self.authToken = self.kl.getAddonSetting('authToken')

        self.connection = Connection(self.ip, self.port)

        self.opt_videoMode = self.kl.getAddonSetting('videoMode')
        self.detection_3d = self.kl.getAddonSetting('detection_3d')
        self.opt_audioMode = self.kl.getAddonSetting('audioMode')
        self.opt_pauseMode = self.kl.getAddonSetting('pauseMode')
        self.opt_menuMode = self.kl.getAddonSetting('menuMode')
        self.opt_screenSaverMode = self.kl.getAddonSetting('screenSaverMode')

        self.moodcolor_1 = self.kl.getAddonSetting('moodcolor_1')
        self.moodcolor_2 = self.kl.getAddonSetting('moodcolor_2')
        self.moodcolor_3 = self.kl.getAddonSetting('moodcolor_3')

        createImage(32, 32, self.moodcolor_1, os.path.join(ADDON_PATH, 'resources', 'media', self.moodcolor_1))
        createImage(32, 32, self.moodcolor_2, os.path.join(ADDON_PATH, 'resources', 'media', self.moodcolor_2))
        createImage(32, 32, self.moodcolor_3, os.path.join(ADDON_PATH, 'resources', 'media', self.moodcolor_3))

        self.monitor.settingsChanged = False

        self.kl.writeLog('Host:                 %s:%s' % (self.ip, self.port))
        self.kl.writeLog('Enable Hyp. on Start: %s' % self.enableHyperion)
        self.kl.writeLog('Disable Hyp. on Stop: %s' % self.disableHyperion)
        self.kl.writeLog('Auth Token:           %s' % self.authToken)
        self.kl.writeLog('Video Mode:           %s' % self.opt_videoMode)
        self.kl.writeLog('3D Autodetection:     %s' % self.detection_3d)
        self.kl.writeLog('Audio Mode:           %s' % self.opt_audioMode)
        self.kl.writeLog('Pause Mode:           %s' % self.opt_pauseMode)
        self.kl.writeLog('Menu Mode:            %s' % self.opt_menuMode)
        self.kl.writeLog('Screensaver Mode:     %s' % self.opt_screenSaverMode)
        self.kl.writeLog('Mood Color 1:         %s' % self.moodcolor_1)
        self.kl.writeLog('Mood Color 2:         %s' % self.moodcolor_2)
        self.kl.writeLog('Mood Color 3:         %s' % self.moodcolor_3)


    def start(self):
        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(1):
                if self.disableHyperion: self.connection.sendComponentState('ALL', False)
                break
            if self.monitor.settingsChanged: self.getSettings()
            self.checkColors()
            mode = self.kl.jsonrpc({"method": "GUI.GetProperties", "params": {"properties": ["stereoscopicmode"]}})
            if mode['stereoscopicmode']['mode'] != self.stereomode:
                self.stereomode = mode['stereoscopicmode']['mode']
                self.connection.sendVideoMode({'split_horizontal': '3DTAB',
                                               'split_vertical': '3DSBS',
                                               'off': '2D'}.get(self.stereomode, 'off'))

                self.kl.writeLog('View mode changed to: %s' % self.stereomode)


if __name__ == '__main__':
        hyperion = Hyperion()
        del hyperion
