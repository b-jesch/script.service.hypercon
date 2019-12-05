from resources.lib.toollib import *
from resources.lib.connection import Connection


class Player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.isPlaying = False
        self.eventChanged = False

    def onPlayBackPaused(self):
        self.isPlaying = True
        self.isPausing = True
        self.eventChanged = True

    def onPlayBackResumed(self):
        self.isPlaying = True
        self.isPausing = False
        self.eventChanged = True

    def onPlayBackEnded(self):
        self.isPlaying = False
        self.isPausing = False
        self.eventChanged = True

    def onPlayBackStarted(self):
        self.isPlaying = True
        self.isPausing = False
        self.eventChanged = True

    def onPlayBackStopped(self):
        self.isPlaying = False
        self.isPausing = False
        self.eventChanged = True

class Monitor(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.screenSaverActive = False
        self.settingsChanged = False
        self.eventChanged = True

    def onScreensaverActivated(self):
        self.screenSaverActive = True
        self.eventChanged = True

    def onScreensaverDeactivated(self):
        self.screenSaverActive = False
        self.eventChanged = True

    def onSettingsChanged(self):
        self.settingsChanged = True


class Hyperion(object):
    def __init__(self):
        self.player = Player()
        self.monitor = Monitor()
        self.kl = KodiLib()

        if not os.path.exists(os.path.join(ADDON_PATH, 'resources', 'media')):
            os.mkdir(os.path.join(ADDON_PATH, 'resources', 'media'))

        self.kl.setProperty('moodcolor_1', self.kl.getAddonSetting('moodcolor_1'))
        self.kl.setProperty('moodcolor_2', self.kl.getAddonSetting('moodcolor_2'))
        self.kl.setProperty('moodcolor_3', self.kl.getAddonSetting('moodcolor_3'))

        self.getSettings()
        self.checkColors()
        self.start()


    def checkColors(self):
        if self.kl.getProperty('moodcolor_1') != self.moodcolor_1:
            ADDON.setSetting('moodcolor_1', self.kl.getProperty('moodcolor_1'))
        if self.kl.getProperty('moodcolor_2') != self.moodcolor_2:
            ADDON.setSetting('moodcolor_2', self.kl.getProperty('moodcolor_2'))
        if self.kl.getProperty('moodcolor_3') != self.moodcolor_3:
            ADDON.setSetting('moodcolor_3', self.kl.getProperty('moodcolor_3'))

    def getSettings(self):
        self.ip = self.kl.getAddonSetting('ip')
        self.port = self.kl.getAddonSetting('port')
        self.enableHyperion = self.kl.getAddonSetting('enableHyperion', sType=BOOL)
        self.disableHyperion = self.kl.getAddonSetting('disableHyperion', sType=BOOL)

        self.connection = Connection(self.ip, self.port)

        self.opt_videoMode = self.kl.getAddonSetting('videoMode')
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

        self.effect_1 = self.kl.getAddonSetting('effect_1')
        self.effect_2 = self.kl.getAddonSetting('effect_2')
        self.effect_3 = self.kl.getAddonSetting('effect_3')
        
        self.monitor.settingsChanged = False

        self.kl.writeLog('Host:                 %s:%s' % (self.ip, self.port))
        self.kl.writeLog('Enable Hyp. on Start: %s' % self.enableHyperion)
        self.kl.writeLog('Disable Hyp. on Stop: %s' % self.disableHyperion)
        self.kl.writeLog('Video Mode:           %s' % self.opt_videoMode)
        self.kl.writeLog('Audio Mode:           %s' % self.opt_audioMode)
        self.kl.writeLog('Pause Mode:           %s' % self.opt_pauseMode)
        self.kl.writeLog('Menu Mode:            %s' % self.opt_menuMode)
        self.kl.writeLog('Screensaver Mode:     %s' % self.opt_screenSaverMode)
        self.kl.writeLog('Mood Color 1:         %s' % self.moodcolor_1)
        self.kl.writeLog('Mood Color 2:         %s' % self.moodcolor_2)
        self.kl.writeLog('Mood Color 3:         %s' % self.moodcolor_3)
        self.kl.writeLog('Effect 1:             %s' % self.effect_1)
        self.kl.writeLog('Effect 2:             %s' % self.effect_2)
        self.kl.writeLog('Effect 3:             %s' % self.effect_3)
        
    def eventHandler(self):
        if self.kl.getProperty('hyperion.status') == 'on':
            if self.monitor.eventChanged or self.player.eventChanged:
                if self.player.isPlaying:
                    if self.player.isPausing:
                        # state paused
                        pass
                    else:
                        # state playing video or audio
                        pass
                else:
                    # state menue or screensaver
                    if self.monitor.screenSaverActive:
                        # state screensaver
                        pass
                    else:
                        # state menue
                        pass
            self.monitor.eventChanged = False
            self.player.eventChanged = False


    def start(self):
        self.kl.writeLog('Starting Hyperion service script', xbmc.LOGNOTICE)

        self.connection.getActiveEffects()
        self.connection.getActiveLedColors()

        if self.enableHyperion:
            self.connection.clearAll()
            self.kl.setProperty('hyperion.status', 'on')

        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(2):
                if self.disableHyperion:
                    self.connection.setColor('#000000')
                    self.kl.setProperty('hyperion.status', 'off')
                break

            if self.monitor.settingsChanged: self.getSettings()
            self.checkColors()

if __name__ == '__main__':
        hyperion = Hyperion()
        del hyperion
