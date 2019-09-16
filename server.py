import random
import string
import cherrypy
import numpy as np
import json

class DynamicProcess():
    def __init__(self):
        self.dimension = 2
        self.__zero_init()
        
    def __zero_init(self):
        self.__y = np.zeros([self.dimension, self.dimension])
        self.__x = np.zeros([self.dimension, self.dimension])

        self.coeff = {'A': np.zeros([self.dimension, self.dimension]),
                      'GAMMA': np.zeros([self.dimension, self.dimension]),
                      'C': np.zeros([self.dimension, self.dimension])
                      }

    def set_value(self, u):
        self.__x = np.dot(self.coeff['A'], self.__x) + np.dot(self.coeff['GAMMA'], u)
        self.__y = np.dot(self.coeff['C'], self.__x)

    def get_value(self):
        return self.__y

    def set_dimension(self, dimension):
        self.dimension = dimension
        self.__zero_init()


class Measurement():
    def __init__(self, dynamic_process):
        self.dynamic_process = dynamic_process

    def read_value(self):
        return str(self.dynamic_process.get_value())


class Controller():
    def __init__(self, dynamic_process):
        self.dynamic_process = dynamic_process

    def set_value(self, value):
        self.dynamic_process.set_value(value)


@cherrypy.expose
class MeasureControlWebService(object):

    def __init__(self, dynamic_process):
        self.measurement = Measurement(dynamic_process)
        self.controller = Controller(dynamic_process)

    def GET(self):
        return self.measurement.read_value()

    def PUT(self, value):
        u = [float(i) for i in value.split()]
        u = np.array(u)
        if np.shape(u)==(self.controller.dynamic_process.dimension,):
            self.controller.set_value(u)

@cherrypy.expose
class CoefficientsWebService(object):

    def __init__(self, dynamic_process):
        self.__dynamic_process = dynamic_process

    def GET(self, type):
        coeff = self.__dynamic_process.coeff[type]
        return np.array_str(coeff) 

    def PUT(self, type, value):
        value = json.loads(value)
        value = np.array(value)
        if np.shape(value) == (self.__dynamic_process.dimension, 
                self.__dynamic_process.dimension):
            self.__dynamic_process.coeff[type] = value

@cherrypy.expose
class DimensionWebService(object):

    def __init__(self, dynamic_process):
        self.__dynamic_process = dynamic_process

    def GET(self):
        return str(self.__dynamic_process.dimension)

    def PUT(self, value):
        self.__dynamic_process.dimension = int(value)



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
    cherrypy.tree.mount(MeasureControlWebService(dynamic_process), '/in_out/',
                        conf)
    cherrypy.tree.mount(CoefficientsWebService(dynamic_process),
                        '/coefficients/', conf)

    cherrypy.tree.mount(DimensionWebService(dynamic_process),
                        '/dimension/', conf)


    cherrypy.engine.start()
    cherrypy.engine.block()
