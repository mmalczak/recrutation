import random
import string

import cherrypy


class DynamicProcess():
    def __init__(self):
        self.__y = 0
    
    def set_value(self, value):
        self.__y = self.__y + value

    def get_value(self):
        return self.__y

class Measurement():
    def __init__(self, dynamic_process):
        self.__dynamic_process = dynamic_process

    def read_value(self):
        return str(self.__dynamic_process.get_value())

class Controller():
    def __init__(self, dynamic_process):
        self.__dynamic_process = dynamic_process

    def set_value(self, value):
        self.__dynamic_process.set_value(value)



@cherrypy.expose
class MeasureControlWebService(object):

    def __init__(self):
        dynamic_process = DynamicProcess()
        self.__measurement = Measurement(dynamic_process)
        self.__controller = Controller(dynamic_process)

    def GET(self):
        return self.__measurement.read_value() 
    
    def PUT(self, value):
        self.__controller.set_value(float(value))


if __name__ == '__main__':
    dynamic_process = DynamicProcess()
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.server.socket_host = '20.0.0.2' 
#    cherrypy.quickstart(MeasureControlWebService(), '/', conf)
    cherrypy.quickstart(MeasureControlWebService(), '/in_out/', conf)
