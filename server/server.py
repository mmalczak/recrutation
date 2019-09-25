import random
import string
import numpy as np
from numpy import matrix
from numpy import dot
from numpy import zeros
from numpy import transpose
import json

import logging
import logging.config
from logging_conf import DEFAULT_CONFIG
logging.config.dictConfig(DEFAULT_CONFIG)
logger = logging.getLogger(__name__)

from flask import Flask, request
from flask_restplus import Resource, Api

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

app = Flask(__name__)
api = Api(app=app, title='Server', description='Provides an API to control\
        the dynamic process' )

def np_to_json(data):
    if type(data) == int:
        return json.dumps(data)
    else:
        return json.dumps(data.tolist())

def json_to_np(data):
    return np.matrix(json.loads(data))


def unity(x):
    return x

def sin(x):
    return np.sin(x)

def pow2(x):
    return np.power(x, 2)

def pow3(x):
    return np.power(x, 3)

def exp(x):
    return np.exp(x)

nonlinearities = {'unity':unity, 'sin':sin, 'pow2':pow2, 'pow3':pow3, 'exp':exp}

class DynamicProcess():
    def __init__(self):
        self.nonlinearity = unity
        self.num_states = 0
        self.num_outputs = 0
        self.delay = 0
        self.error_dist_mu = 0
        self.error_dist_sigma = 0.1
        self.__zero_init()

    def __zero_init(self):
        self.__y = transpose(matrix(zeros([self.num_outputs])))
        self.__x = transpose(matrix(zeros([self.num_states])))
        self.coeff = {'A': None,
                      'B': None,
                      'C': None,
                      }
        self.fifo = []
        for i in range(self.delay):
            self.fifo.append(self.__y)



    def set_value(self, u):
        self.__x = dot(self.coeff['A'], self.__x) + dot(self.coeff['B'], u)
        output = dot(self.coeff['C'], self.nonlinearity(self.__x)) +\
            transpose(matrix(np.random.normal(self.error_dist_mu,
            self.error_dist_sigma, self.num_outputs)))
        self.fifo.append(output)
        self.__y = self.fifo.pop(0)
        logger.info("state: {}".format(self.__x))
        logger.info("out: {}".format(self.__y))
        logger.info("=================================================")

    def get_value(self):
        return np_to_json(self.__y)

    def set_num_states(self, num_states):
        self.num_states = num_states
        self.__zero_init()

    def set_num_outputs(self, num_outputs):
        self.num_outputs = num_outputs
        self.__zero_init()

    def set_delay(self, delay):
        self.delay = delay
        logger.info('delay= {}'.format(delay))
        self.__zero_init()

    def set_nonlinearity(self, nonlinearity):
        self.nonlinearity = nonlinearities[nonlinearity]


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


dynamic_process = DynamicProcess()
measurement = Measurement(dynamic_process)
controller = Controller(dynamic_process)


@api.route('/in_out')
class MeasureControlWebService(Resource):

    def get(self):
        return measurement.read_value()

    @api.doc(params={'control_signal': 'The signal used to control the dynamic\
                                        process'})
    def post(self):
        value = request.form['data']
        u = json_to_np(value)
        controller.set_value(u)

@api.route('/coefficients/<string:type>')
@api.doc(params={'type': 'Name of the matrix to modify'})
class CoefficientsWebService(Resource):

    def get(self, type):
        coeff = dynamic_process.coeff[type]
        return np_to_json(coeff)

    @api.doc(params={'coeff': 'Values of the requested matrix'})
    def put(self, type):
        value = request.form['data']
        value = json_to_np(value)
        dynamic_process.coeff[type] = value

@api.route('/num_states')
class NumStatesWebService(Resource):

    def get(self):
        return str(dynamic_process.num_states)

    @api.doc(params={'num_states': 'Number of states in the dynamic process'})
    def put(self):
        num_states = request.form['data']
        dynamic_process.set_num_states(int(num_states))

@api.route('/num_outputs')
class NumOutputsWebService(Resource):

    def get(self):
        return str(dynamic_process.num_outputs)

    @api.doc(params={'num_outputs': 'Number of outputs/inputs of the dynamic\
                                     process'})
    def put(self):
        num_outputs= request.form['data']
        dynamic_process.set_num_outputs(int(num_outputs))

@api.route('/delay')
class DelayWebService(Resource):

    def get(self):
        return str(dynamic_process.delay)

    @api.doc(params={'delay': 'Delay of the dynamic process\' output (in\
                               number of samples)'})
    def put(self):
        delay = request.form['data']
        dynamic_process.set_delay(int(delay))

@api.route('/nonlinearity')
class NonlinearityWebService(Resource):

    @api.doc(params={'nonlinearity': 'The function used to introduce the\
                                      nonlinearity in the system. Available\
                                      values: unity, sin, pow2, pow3, exp'})
    def put(self):
        nonlinearity = request.form['data']
        dynamic_process.set_nonlinearity(nonlinearity)

@api.route('/error_dist/mu')
class ErrorMuWebService(Resource):

    def get(self):
        return str(dynamic_process.error_dist_mu)

    @api.doc(params={'mu': 'Value of the noise normal distribution\
                            expectation'})
    def put(self):
        mu = request.form['data']
        dynamic_process.error_dist_mu = float(mu)

@api.route('/error_dist/sigma')
class ErrorSigmaWebService(Resource):

    def get(self):
        return str(dynamic_process.error_dist_sigma)

    @api.doc(params={'sigma': 'Value of the noise normal distribution\
                               sigma'})
    def put(self):
        sigma = request.form['data']
        dynamic_process.error_dist_sigma = float(sigma)



app.config["SERVER_NAME"] = "20.0.0.2:5000"
app.app_context().__enter__()
with open('server_API.json', 'w') as file:
    file.write(json.dumps(api.__schema__, indent=2))
    file.close()

if __name__ == '__main__':
    app.run(host='20.0.0.2')
