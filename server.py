import random
import string
import cherrypy
import numpy as np
from numpy import matrix
from numpy import dot
from numpy import zeros
from numpy import transpose
import json


def np_to_json(data):
        return json.dumps(data.tolist())

def json_to_np(data):
    return np.matrix(json.loads(data))


class DynamicProcess():
    def __init__(self):
        self.dimension = 2
        self.__zero_init()

    def __zero_init(self):
        self.__y = transpose(matrix(zeros([self.dimension])))
        self.__x = transpose(matrix(zeros([self.dimension])))


        self.coeff = {'A': zeros([self.dimension, self.dimension]),
                      'B': transpose(matrix(zeros([self.dimension]))),
                      'C': zeros([self.dimension, self.dimension])
                      }

    def set_value(self, u):
        print("B: {}".format(self.coeff['B']))
        print("u: {}".format(u))
        self.__x = dot(self.coeff['A'], self.__x) + dot(self.coeff['B'], u)
        print('state = {}'.format(self.__x))
        self.__y = dot(self.coeff['C'], self.__x) + transpose(matrix([np.random.normal(0, 0.1), 0]))
        print('y = {}'.format(self.__y))

    def get_value(self):
        return np_to_json(self.__y)

    def set_dimension(self, dimension):
        self.dimension = dimension
        self.__zero_init()


class Measurement():
    def __init__(self, dynamic_process):
        self.dynamic_process = dynamic_process

    def read_value(self):
        return self.dynamic_process.get_value()


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
        u = json_to_np(value)
        if np.shape(u)==(1, self.controller.dynamic_process.dimension):
            self.controller.set_value(u)

@cherrypy.expose
class CoefficientsWebService(object):

    def __init__(self, dynamic_process):
        self.__dynamic_process = dynamic_process

    def GET(self, type):
        coeff = self.__dynamic_process.coeff[type]
        return np_to_json(coeff)

    def PUT(self, type, value):
        value = json_to_np(value)
        if np.shape(value) == (self.__dynamic_process.dimension,
                self.__dynamic_process.dimension):
            self.__dynamic_process.coeff[type] = value
        elif np.shape(value) == (1, self.__dynamic_process.dimension):
            self.__dynamic_process.coeff[type] = transpose(value)
        else:
            print("ERROR")

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
