import random
import string

import cherrypy


class System():
    def __init__(self):
        self.__y = 0
    
    def set_value(self, value):
        self.__y = self.__y + value

    def get_value(self):
        return self.__y

class Measurement():
    def __init__(self, system):
        self.__system = system

    def read_value(self):
        return str(self.__system.get_value())

class Controller():
    def __init__(self, system):
        self.__system = system

    def set_value(self, value):
        self.__system.set_value(value)



@cherrypy.expose
class MeasureControlWebService(object):

    def __init__(self):
        system = System()
        self.__measurement = Measurement(system)
        self.__controller = Controller(system)

    def GET(self):
        return self.__measurement.read_value() 
    
    def PUT(self, value):
        self.__controller.set_value(float(value))


if __name__ == '__main__':
    system = System()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.server.socket_host = '20.0.0.2' 
    cherrypy.quickstart(MeasureControlWebService(), '/', conf)
