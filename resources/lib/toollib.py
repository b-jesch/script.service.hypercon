import random
import xbmcgui
import xbmcaddon
import xbmc
import json
import re
import platform
import os

from contextlib import contextmanager
from PIL import Image

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_PATH = xbmc.translatePath(ADDON.getAddonInfo('path'))
LS = ADDON.getLocalizedString

# Constants

STRING = 0
BOOL = 1
NUM = 2


class CryptDecrypt(object):
    '''
    :param passw: ID/Name of the associated password item in settings.xml
    :param key: ID of the associated key in settings, will be generated at first run
    :param token: ID of the token in settings, generated from password/key
    :return: decrypted password if password in settings is empty or *, else set password to '*' and generates key/token,
             stores password into settings.xml, key/token within userdata/addon_data/addon_id/settings.xml
    '''

    def __init__(self, passw, key, token):

        self.passw = ADDON.getSetting(passw)

        self.__pw_item = passw
        self.__key = ADDON.getSetting(key)
        self.__key_item = key
        self.__token = ADDON.getSetting(token)
        self.__token_item = token

    def persist(self):
        ADDON.setSetting(self.__key_item, self.__key)
        ADDON.setSetting(self.__token_item, self.__token)
        ADDON.setSetting(self.__pw_item, '*')

    def crypt(self):

        if self.passw == '' or self.passw == '*':
            if len(self.__key) > 2: return "".join(
                [chr(ord(self.__token[i]) ^ ord(self.__key[i])) for i in range(int(self.__key[-2:]))])
            return ''
        else:
            self.__key = ''
            for i in range((int(len(self.passw) / 16)) + 1):
                self.__key += ('%016d' % int(random.random() * 10 ** 16))
            self.__key = self.__key[:-2] + ('%02d' % len(self.passw))
            __tpw = self.passw.ljust(len(self.__key), 'a')

            self.__token = "".join([chr(ord(__tpw[i]) ^ ord(self.__key[i])) for i in range(len(self.__key))])
            self.persist()
            return self.passw


class OsRelease(object):

    def __init__(self):
        self.platform = platform.system()
        self.hostname = platform.node()
        item = {}
        if self.platform == 'Linux':

            try:
                with open('/etc/os-release', 'r') as _file:
                    for _line in _file:
                        parameter, value = _line.split('=')
                        item[parameter] = value
            except IOError as e:
                KodiLib.writeLog(e.message, xbmc.LOGERROR)

        self.osname = item.get('NAME', 'unknown')
        self.osid = item.get('ID', 'unknown')
        self.osversion = item.get('VERSION_ID', 'unknown')


class KodiLib(object):
    '''
    several Kodi routines and functions
    '''

    def __init__(self):
        self.OSD = xbmcgui.Dialog()

    def __strToBool(self, par):
        return True if par.upper() == 'TRUE' else False

    def writeLog(self, message, level=xbmc.LOGDEBUG):
        try:
            xbmc.log('[%s %s]: %s' % (ADDON_ID, ADDON_VERSION, message), level)
        except Exception:
            xbmc.log('[%s %s]: %s' % (ADDON_ID, ADDON_VERSION, 'Fatal: Could not log message'), xbmc.LOGERROR)

    def jsonrpc(self, query):
        querystring = {"jsonrpc": "2.0", "id": 1}
        querystring.update(query)
        try:
            response = json.loads(xbmc.executeJSONRPC(json.dumps(querystring, encoding='utf-8')))
            if 'result' in response: return response['result']
        except TypeError as e:
            self.writeLog('Error executing JSON RPC: %s' % (e.args), xbmc.LOGERROR)
        return False

    def getAddonSetting(self, setting, sType=STRING, multiplicator=1):
        if sType == BOOL:
            return self.__strToBool(ADDON.getSetting(setting))
        elif sType == NUM:
            try:
                return int(re.findall('([0-9]+)', ADDON.getSetting(setting))[0]) * multiplicator
            except (IndexError, TypeError, AttributeError) as e:
                self.writeLog('Could not get setting type NUM for %s, return with 0' % (setting), xbmc.LOGERROR)
                self.writeLog(str(e.message))
                return 0
        else:
            return ADDON.getSetting(setting)

    def notifyOSD(self, header, message, time=5000, icon=xbmcgui.NOTIFICATION_INFO):
        self.OSD.notification(LS(header), LS(message), icon, time)

    def ParamsToDict(self, parameters):
        params = dict()
        if parameters:
            pairs = parameters.split("&")
            for pair in pairs:
                key_value = pair.split('=')
                if (len(key_value)) == 2:
                    params.update({key_value[0]: key_value[1]})
        return params


    def setProperty(self, property, value):
        xbmcgui.Window(10000).setProperty(str(property), str(value))

    def getProperty(self, property):
        return xbmcgui.Window(10000).getProperty(str(property))

    '''
    creates a replacement for busy dialog in Kodi V.18 (Leia) build a wrapper function for this. The wrapper
    guarantees that the busy dialog will be closed whatever happens inside the with block.

    use it as follows:

    with busy_dialog:
        # script here whatever you want
    '''

    @contextmanager
    def busy_dialog(self):
        xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
        try:
            yield
        finally:
            xbmc.executebuiltin('Dialog.Close(busydialognocancel)')


class KlProgressBar(object):
    '''
    creates a dialog progressbar with optional reverse progress
        :param header: heading line of progressbar
        :param msg: additional countdown message
        :param duration: duration of countdown
        :param steps: amount of steps of the countdown, choosing a value of 2*duration is perfect (actualising every 500 msec)
        :param reverse: reverse countdown (progressbar from 100 to 0)

        :returns true if cancel button was pressed, otherwise false
    '''

    def __init__(self, header, msg, duration=5, steps=10, reverse=False):

        self.header = header
        self.msg = msg
        self.timeout = int(1000 * duration / steps)
        self.steps = int(100 / steps)
        self.reverse = reverse
        self.iscanceled = False

        self.pb = xbmcgui.DialogProgress()

        self.max = 0
        if self.reverse: self.max = 100

        self.pb.create(self.header, self.msg)
        self.pb.update(self.max, self.msg)

    def show_progress(self):

        percent = 100
        while percent >= 0:
            self.pb.update(self.max, self.msg)
            if self.pb.iscanceled():
                self.iscanceled = True
                break

            percent -= self.steps
            self.max = 100 - percent
            if self.reverse: self.max = percent
            xbmc.sleep(self.timeout)

        self.pb.close()
        return self.iscanceled


def createImage(width, height, rgbColor, path):
    """
    Creates an RGB image and store it into path
    :param width:       width of image in pixel
    :param height:      height of image in pixel
    :param rgbColor:    color of the background in #RRGGBB hex notation
    :param path:        Path/Name of image
    :return:            True if successful
    """

    if os.path.exists(path): return path
    rgb = rgbColor.lstrip('#')
    # skip transparency
    if len(rgb) == 8: rgb = rgb[2:8]
    lv = len(rgb)
    color = tuple(int(rgb[i:i + lv / 3], 16) for i in range(0, lv, lv / 3))
    img = Image.new('RGB', (width, height), color)
    img.save(path, format='PNG')
    return path