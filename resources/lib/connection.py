import httplib2


class Connection(object):

    def __init__(self):
        self.__http = httplib2.Http()
        self.__header = {'Content-type': 'application/json'}
        self.__url = self.updateURL()


    def updateHeader(self, authToken):
        if authToken == "" and not self.__headers.key('Authorization'):
            self.__headers.pop('Authorization')
        elif not self.__headers.key('Authorization'):
            self.__headers = self.__headers.update({'Authorization' : 'token %s' % authToken})


    def updateURL(self, ip='127.0.0.1', port='8090'):
        self.__url = 'http://%s:%s/json-rpc' % (ip, port)


    def send(self, body):
        try:
            response, content = self.__http.request(self.__url, 'POST', headers=self.__header, body=body)
        except httplib2.HttpLib2Error as e:
            print (e.message)


    def sendComponentState(self, component, state):
        self.send('{"command":"componentstate", "componentstate":{"component":"%s", "state":"%s", "tan":1}' % (component, state.lower()))


    def sendVideoMode(self, mode):
        self.send('{"command":"videoMode", "videoMode":"%s", "tan":1}' % mode)
