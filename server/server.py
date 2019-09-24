import random
import string
import numpy as np
from numpy import matrix
from numpy import dot
from numpy import zeros
from numpy import transpose
import json

from flask import Flask, request
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)


def np_to_json(data):
    if type(data) == int:
        return json.dumps(data)
    else:
        return json.dumps(data.tolist())

def json_to_np(data):
    return np.matrix(json.loads(data))


def unity(x):
    return x

class DynamicProcess():
    def __init__(self):
        #self.nonlinearity = np.sin
        self.nonlinearity = unity
        self.num_states = 0
        self.num_outputs = 0
        self.__zero_init()

    def __zero_init(self):
        self.__y = transpose(matrix(zeros([self.num_outputs])))
        self.__x = transpose(matrix(zeros([self.num_states])))
        self.coeff = {'A': None,
                      'B': None,
                      'C': None,
                      }

    def set_value(self, u):
        self.__x = dot(self.coeff['A'], self.__x) + dot(self.coeff['B'], u)
        self.__y = dot(self.coeff['C'], self.nonlinearity(self.__x)) + np.random.normal(0, 0.1)
        print("state: {}".format(self.__x))
        print("out: {}".format(self.__y))
        print("=================================================")

    def get_value(self):
        return np_to_json(self.__y)

    def set_num_states(self, num_states):
        self.num_states = num_states
        self.__zero_init()

    def set_num_outputs(self, num_outputs):
        self.num_outputs = num_outputs
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


dynamic_process = DynamicProcess()
measurement = Measurement(dynamic_process)
controller = Controller(dynamic_process)


@api.route('/in_out')
class MeasureControlWebService(Resource):

    def get(self):
        return measurement.read_value()

    def put(self):
        value = request.form['data']
        u = json_to_np(value)
        controller.set_value(u)

@api.route('/coefficients/<string:type>')
class CoefficientsWebService(Resource):

    def get(self, type):
        coeff = dynamic_process.coeff[type]
        return np_to_json(coeff)

    def put(self, type):
        value = request.form['data']
        value = json_to_np(value)
        dynamic_process.coeff[type] = value

@api.route('/num_states')
class NumStatesWebService(Resource):

    def get(self):
        return str(dynamic_process.num_states)

    def put(self):
        num_states = request.form['data']
        dynamic_process.set_num_states(int(num_states))

@api.route('/num_outputs')
class NumOutputsWebService(Resource):

    def get(self):
        return str(dynamic_process.num_outputs)

    def put(self):
        num_outputs= request.form['data']
        dynamic_process.set_num_outputs(int(num_outputs))

app.config["SERVER_NAME"] = "20.0.0.2:5000"
app.app_context().__enter__()
with open('server_API.json', 'w') as file:
    file.write(json.dumps(api.__schema__, indent=2))
    file.close()

if __name__ == '__main__':
    app.run(host='20.0.0.2')
