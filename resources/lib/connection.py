import websocket
import socket
import json
from toollib import KodiLib


class Connection(object):

    def __init__(self, ip='127.0.0.1', port='19444'):
        self.__kl = KodiLib()
        self.__header = {'Content-type': 'application/json'}
        self.__url = 'ws://%s:%s' % (ip, port)

    def send(self, payload):
        try:
            self.__ws = websocket.create_connection(self.__url, timeout=3)
            self.__kl.writeLog('send %s' % payload)
            self.__ws.send(payload)
            response = json.loads(self.__ws.recv(), encoding='utf-8')
            self.__ws.close()
            return (bool(response.get('success', False)), response.get('info', response.get('error', None)))

        except (websocket.error, socket.timeout):
            self.__kl.notifyOSD(32000, 32060)

        return (False, None)

    def getActiveEffects(self):
        success, response = self.send('{"command": "serverinfo"}')
        if success:
            _ae = False
            for effect in response['activeEffects']:
                self.__kl.writeLog('active effect: %s' % effect.get('name', None))
                _ae = True
            if not _ae: self.__kl.writeLog('no active Effects')

            _al = False
            for led in response['activeLedColor']:
                self.__kl.writeLog('active LED color: %s' % led.get('HEX Value', None))
                _al = True
            if not _al: self.__kl.writeLog('no active LEDs')

    def Clear(self, priority=100):
        self.__kl.writeLog('success: %s %s' % self.send('{"command": "effect", "effect": {"name": "clear"}, "priority": %s}' % priority))

    def clearAll(self):
        self.__kl.writeLog('success: %s %s' % self.send('{"command": "clearall"}'))

    def setColor(self, rgbcolor, priority=100):

        # skip leading '#' and transparency

        rgbcolor = rgbcolor.lstrip('#')
        if len(rgbcolor) > 6: rgbcolor = rgbcolor[-6:]

        red, green, blue = tuple(int(rgbcolor[i:i + 2], 16) for i in range(0, 6, 2))
        self.__kl.writeLog('success: %s %s' %
                           self.send('{"command": "color", "priority": %s, "color": [%s, %s, %s]}' % (priority, red, green, blue)))
