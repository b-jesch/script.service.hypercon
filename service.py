from resources.lib.toollib import *
from resources.lib.connection import Connection

kl = KodiLib()


class Player(xbmc.Player):
    def __init__(self):
        xbmc.Player.__init__(self)
        self.isPlaying = False
        self.isPausing = False
        self.eventChanged = True

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
        self.eventChanged = False

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
        kl.setProperty('hyperion.check', '-1')

        if not os.path.exists(os.path.join(ADDON_PATH, 'resources', 'media')):
            os.mkdir(os.path.join(ADDON_PATH, 'resources', 'media'))

        kl.setProperty('moodcolor_1', kl.getAddonSetting('moodcolor_1'))
        kl.setProperty('moodcolor_2', kl.getAddonSetting('moodcolor_2'))
        kl.setProperty('moodcolor_3', kl.getAddonSetting('moodcolor_3'))

        self.getSettings()
        self.checkColors()
        self.start()

    def checkColors(self):
        if kl.getProperty('moodcolor_1') != self.moodcolor_1:
            ADDON.setSetting('moodcolor_1', kl.getProperty('moodcolor_1'))
        if kl.getProperty('moodcolor_2') != self.moodcolor_2:
            ADDON.setSetting('moodcolor_2', kl.getProperty('moodcolor_2'))
        if kl.getProperty('moodcolor_3') != self.moodcolor_3:
            ADDON.setSetting('moodcolor_3', kl.getProperty('moodcolor_3'))

    def getSettings(self):
        self.ip = kl.getAddonSetting('ip')
        self.port = kl.getAddonSetting('port')
        self.enableHyperion = kl.getAddonSetting('enableHyperion', sType=BOOL)
        self.disableHyperion = kl.getAddonSetting('disableHyperion', sType=BOOL)

        self.connection = Connection(self.ip, self.port)

        self.opt_videoMode = kl.getAddonSetting('videoMode', sType=NUM)
        self.opt_audioMode = kl.getAddonSetting('audioMode', sType=NUM)
        self.opt_pauseMode = kl.getAddonSetting('pauseMode', sType=NUM)
        self.opt_menuMode = kl.getAddonSetting('menuMode', sType=NUM)
        self.opt_screenSaverMode = kl.getAddonSetting('screenSaverMode', sType=NUM)

        self.moodcolor_1 = kl.getAddonSetting('moodcolor_1')
        self.moodcolor_2 = kl.getAddonSetting('moodcolor_2')
        self.moodcolor_3 = kl.getAddonSetting('moodcolor_3')
        createImage(32, 32, self.moodcolor_1, os.path.join(ADDON_PATH, 'resources', 'media', self.moodcolor_1))
        createImage(32, 32, self.moodcolor_2, os.path.join(ADDON_PATH, 'resources', 'media', self.moodcolor_2))
        createImage(32, 32, self.moodcolor_3, os.path.join(ADDON_PATH, 'resources', 'media', self.moodcolor_3))

        self.effect_1 = kl.getAddonSetting('effect_1')
        self.effect_2 = kl.getAddonSetting('effect_2')
        self.effect_3 = kl.getAddonSetting('effect_3')
        
        self.monitor.settingsChanged = False

        kl.writeLog('Host:                 %s:%s' % (self.ip, self.port))
        kl.writeLog('Enable Hyp. on Start: %s' % self.enableHyperion)
        kl.writeLog('Disable Hyp. on Stop: %s' % self.disableHyperion)
        kl.writeLog('Video Mode:           %s' % self.opt_videoMode)
        kl.writeLog('Audio Mode:           %s' % self.opt_audioMode)
        kl.writeLog('Pause Mode:           %s' % self.opt_pauseMode)
        kl.writeLog('Menu Mode:            %s' % self.opt_menuMode)
        kl.writeLog('Screensaver Mode:     %s' % self.opt_screenSaverMode)
        kl.writeLog('Mood Color 1:         %s' % self.moodcolor_1)
        kl.writeLog('Mood Color 2:         %s' % self.moodcolor_2)
        kl.writeLog('Mood Color 3:         %s' % self.moodcolor_3)
        kl.writeLog('Effect 1:             %s' % self.effect_1)
        kl.writeLog('Effect 2:             %s' % self.effect_2)
        kl.writeLog('Effect 3:             %s' % self.effect_3)


    def getPlayerProperties(self):
        query = {
                "method": "Player.GetActivePlayers",
                }
        res = kl.jsonrpc(query)
        return res[0].get('type', None)

    def effectHandler(self, nr=0):
        if nr == 0: self.connection.clearAll()
        elif nr == 1: self.connection.setColor(self.moodcolor_1),
        elif nr == 2: self.connection.setColor(self.moodcolor_2),
        elif nr == 3: self.connection.setColor(self.moodcolor_3),
        elif nr == 4: self.connection.setEffect(self.effect_1),
        elif nr == 5: self.connection.setEffect(self.effect_2),
        elif nr == 6: self.connection.setEffect(self.effect_3),
        elif nr == 7: self.connection.setColor('#000000')
        else:
            pass

    def eventHandler(self, force=False):
        if kl.getProperty('hyperion.status') == 'on':
            if self.monitor.eventChanged or self.player.eventChanged or force:
                if self.player.isPlaying:
                    if self.player.isPausing:
                        # state paused
                        kl.writeLog('player.paused => %s' % self.opt_pauseMode)
                        self.effectHandler(self.opt_pauseMode)
                    else:
                        # state playing video or audio
                        media = self.getPlayerProperties()
                        if media == 'video':
                            kl.writeLog('player.isplaying %s => %s' % (media, self.opt_videoMode))
                            self.effectHandler(self.opt_videoMode)
                        elif media == 'audio':
                            kl.writeLog('player.isplaying %s => %s' % (media, self.opt_audioMode))
                            self.effectHandler(self.opt_audioMode)
                        else:
                            pass
                else:
                    # state menue or screensaver
                    if self.monitor.screenSaverActive:
                        # state screensaver
                        kl.writeLog('screensaver.active => %s' % self.opt_screenSaverMode)
                        self.effectHandler(self.opt_screenSaverMode)
                    else:
                        # state menue
                        kl.writeLog('menu.isShowing => %s' % self.opt_menuMode)
                        self.effectHandler(self.opt_menuMode)

            self.monitor.eventChanged = False
            self.player.eventChanged = False

    def start(self):
        kl.writeLog('Starting Hyperion service script', xbmc.LOGNOTICE)

        self.connection.getActiveEffects()
        self.connection.getActiveLedColors()

        if self.enableHyperion:
            kl.setProperty('hyperion.status', 'on')
            self.eventHandler(force=True)

        while not self.monitor.abortRequested():
            if self.monitor.waitForAbort(2):
                if self.disableHyperion:
                    self.connection.setColor('#000000')
                    kl.setProperty('hyperion.status', 'off')
                break

            if self.monitor.settingsChanged: self.getSettings()
            self.checkColors()
            _checkcounter = int(kl.getProperty('hyperion.check'))
            if _checkcounter > 0:
                _checkcounter -= 1
                kl.setProperty('hyperion.check', str(_checkcounter))
            elif _checkcounter == 0:
                _checkcounter -= 1
                kl.setProperty('hyperion.check', str(_checkcounter))
                kl.writeLog('Return to normal behaviour')
                kl.notifyOSD(32000, 32039)
                self.eventHandler(force=True)
            else:
                pass
            self.eventHandler()


if __name__ == '__main__':
        hyperion = Hyperion()
        del hyperion
