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
    if type(data) == int:
        return json.dumps(data)
    else:
        return json.dumps(data.tolist())

def json_to_np(data):
    return np.matrix(json.loads(data))


class DynamicProcess():
    def __init__(self):
        self.num_states = 2
        self.__zero_init()

    def __zero_init(self):
        self.__y = 0
        self.__x = transpose(matrix(zeros([self.num_states])))


        self.coeff = {'A': None,
                      'B': None,
                      'C': None,
                      }

    def set_value(self, u):
        self.__x = dot(self.coeff['A'], self.__x) + dot(self.coeff['B'], u)
        self.__y = dot(self.coeff['C'], self.__x) + np.random.normal(0, 0.1)
        print("state: {}".format(self.__x))
        print("out: {}".format(self.__y))

    def get_value(self):
        return np_to_json(self.__y)

    def set_num_states(self, num_states):
        self.num_states = num_states
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
        self.__dynamic_process.coeff[type] = value

@cherrypy.expose
class NumStatesWebService(object):

    def __init__(self, dynamic_process):
        self.__dynamic_process = dynamic_process

    def GET(self):
        return str(self.__dynamic_process.num_states)

    def PUT(self, value):
        self.__dynamic_process.set_num_states(int(value))



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

    cherrypy.tree.mount(NumStatesWebService(dynamic_process),
                        '/num_states/', conf)


    cherrypy.engine.start()
    cherrypy.engine.block()
