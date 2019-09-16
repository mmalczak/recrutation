import random
import string
import cherrypy
import numpy as np


class DynamicProcess():
    def __init__(self):
        self.__y = np.array([0, 0])
        self.__x = np.array([0, 0])

        self.__A = np.array([[1, 2],[2, 1]])
        self.__GAMMA = np.array([[1, 1],[1, 1]])
        self.__C = np.array([[1, 0],[0, 1]])

    def set_value(self, u):
        self.__x = np.dot(self.__A, self.__x) + np.dot(self.__GAMMA, u)
        self.__y = np.dot(self.__C, self.__x)

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

    def __init__(self, dynamic_process):
        self.__measurement = Measurement(dynamic_process)
        self.__controller = Controller(dynamic_process)

    def GET(self):
        return self.__measurement.read_value()

    def PUT(self, value):
        u = [float(i) for i in value.split()]
        self.__controller.set_value(u)


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
    cherrypy.quickstart(MeasureControlWebService(dynamic_process), '/in_out/',
                        conf)
