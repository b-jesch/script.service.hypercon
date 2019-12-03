import httplib2
import socket
from toollib import KodiLib


class Connection(object):

    def __init__(self, ip='127.0.0.1', port='19444'):
        self.__kl = KodiLib()
        self.__http = httplib2.Http()
        self.__header = {'Content-type': 'application/json'}
        self.__url = 'http://%s:%s/json-rpc' % (ip, port)


    def updateHeader(self, authToken):
        if authToken == "" and not self.__header.key('Authorization'):
            self.__header.pop('Authorization')
        elif not self.__header.key('Authorization'):
            self.__header = self.__header.update({'Authorization': 'token %s' % authToken})


    def send(self, body):
        try:
            response, content = self.__http.request(self.__url, 'POST', body, self.__header)
            self.__kl.writeLog('Response from %s: %s, %s' % (self.__url, response['status'], content))
        except socket.error as e:
            self.__kl.writeLog('%s: ERROR: %s' % (self.__url, e))


    def sendComponentState(self, component, state):
        self.send('{"command":"componentstate", "componentstate":{"component":"%s", "state":"%s"}, "tan":1}' % (component, state))


    def sendVideoMode(self, mode):
        self.send('{"command":"videoMode", "videoMode":"%s", "tan":1}' % mode)


    def sendColor(self, rgbcolor, priority=100):

        # skip leading '#' and transparency

        rgbcolor = rgbcolor.lstrip('#')
        if len(rgbcolor) > 6: rgbcolor = rgbcolor[2:8]

        red, green, blue = tuple(int(rgbcolor[i:i + 2], 16) for i in range(0, 6, 2))
        self.send('{"command":"color", "priority":"%s", "color":[%s, %s, %s], "tan":1}' % (priority, red, green, blue))
