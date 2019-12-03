import websocket
import json
from toollib import KodiLib


class Connection(object):

    def __init__(self, ip='127.0.0.1', port='19444'):
        self.__kl = KodiLib()
        self.__header = {'Content-type': 'application/json'}
        self.__url = 'ws://%s:%s' % (ip, port)

    def send(self, payload):
        self.__ws = websocket.create_connection(self.__url, timeout=3)
        try:
            self.__kl.writeLog('send %s' % payload)
            self.__ws.send(payload)
            response = self.__ws.recv()
            self.__ws.close()
            return json.loads(response, encoding='utf-8')
        except websocket.error:
            pass

    def sendComponentState(self, component, state):
        self.send('{"command":"componentstate", "componentstate":{"component":"%s", "state":"%s"}}' % (component, state))

    def sendVideoMode(self, mode):
        self.send('{"command": "videoMode", "videoMode": "%s"}' % mode)

    def sendServerInfo(self):
        self.send('{"command": "serverinfo"}')

    def clearAll(self):
        response = self.send('{"command": "clearall"}')
        return bool(response.get('success', False))

    def sendColor(self, rgbcolor, priority=100):

        # skip leading '#' and transparency

        rgbcolor = rgbcolor.lstrip('#')
        if len(rgbcolor) > 6: rgbcolor = rgbcolor[-6:]

        red, green, blue = tuple(int(rgbcolor[i:i + 2], 16) for i in range(0, 6, 2))
        response = self.send('{"command": "color", "priority":%s, "color": [%s, %s, %s]}' % (priority, red, green, blue))
        return bool(response.get('success', False))
