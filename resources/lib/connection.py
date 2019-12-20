import websocket
import socket
import json
from toollib import KodiLib

kl = KodiLib()

class Connection(object):

    def __init__(self, ip='127.0.0.1', port='19444'):
        self.__header = {'Content-type': 'application/json'}
        self.__url = 'ws://%s:%s' % (ip, port)

    def send(self, payload):
        try:
            self.__ws = websocket.create_connection(self.__url, timeout=3)
            kl.writeLog('send %s' % payload)
            self.__ws.send(payload)
            response = json.loads(self.__ws.recv(), encoding='utf-8')
            self.__ws.close()
            return (bool(response.get('success', False)), response.get('info', response.get('error', '')))

        except (websocket.error, socket.timeout, socket.error):
            kl.notifyOSD(32000, 32060)

        return (False, '')


    def getActiveTasks(self):
        success, response = self.send('{"command": "serverinfo"}')
        if success:
            active_tasks = list()
            for effect in response['activeEffects']: active_tasks.append(effect.get('name', None)[0].encode('utf-8'))
            for led in response['activeLedColor']: active_tasks.append(led.get('HEX Value', None)[0].encode('utf-8'))
            kl.writeLog('active Effects/Colors: %s' % str(active_tasks))
            return active_tasks
        return False
            
    def fetchEffectList(self):
        success, response = self.send('{"command": "serverinfo"}')
        if success:
            effect_names = list()
            for effect in response['effects']: effect_names.append(effect.get('name', ''))
            kl.writeLog('Builtin effects: %s' % effect_names)
            return effect_names
        return False

    def Clear(self, priority=100):
        kl.writeLog('success: %s %s' %
                           self.send('{"command": "effect", "effect": {"name": "clear"}, "priority": %s}' % priority))

    def clearAll(self):
        kl.writeLog('success: %s %s' % self.send('{"command": "clearall"}'))

    def setEffect(self, effect, priority=100):
        kl.writeLog('success: %s %s' %
                           self.send('{"command": "effect", "effect": {"name": "%s"}, "priority": %s}' % (effect, priority)))

    def setColor(self, rgbcolor, priority=100):

        # skip leading '#' and transparency

        rgbcolor = rgbcolor.lstrip('#')
        if len(rgbcolor) > 6: rgbcolor = rgbcolor[-6:]

        red, green, blue = tuple(int(rgbcolor[i:i + 2], 16) for i in range(0, 6, 2))
        kl.writeLog('success: %s %s' %
                           self.send('{"command": "color", "priority": %s, "color": [%s, %s, %s]}' % (priority, red, green, blue)))
