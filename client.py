import requests
import json
import time
import numpy as np
from numpy import matrix
from numpy import dot
from numpy import zeros
from numpy import transpose
import scipy.signal
import control


def np_to_json(data):
    if type(data) == int:
        return json.dumps(data)
    else:
        return json.dumps(data.tolist())


def json_to_np(data):
    return np.matrix(json.loads(data))


class DynamicProcessSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://20.0.0.2:8080/'
        self.__dimension = 2

    def get_output(self):
        r = self.__session.get(self.__address + 'in_out/')
        print('r.text: {}'.format(r.text))
        return json.loads(r.text)

    def set_input(self, value):
        r = self.__session.put(self.__address + 'in_out/', data={'value':value})
        print(r.text)

    def get_coefficient(self, type):
        r = self.__session.get(self.__address + 'coefficients/' + type + '/')
        print(r.text)

    def set_coefficient(self, type, value):
        r = self.__session.put(self.__address + 'coefficients/' + type + '/',
                               data={'value':value})
        print(r.text)

    def get_dimension(self):
        r = self.__session.get(self.__address + 'dimension/')
        print(r.text)

    def set_dimension(self, value):
        r = self.__session.put(self.__address + 'dimension/',
                               data={'value':value})
        print(r.text)

class Controller():
    def __init__(self):
        self.dimension = 2
        self.__zero_init()

    def __zero_init(self):
        self.x_est = matrix(zeros([self.dimension])).transpose()
        self.u = 0 #matrix(zeros([self.dimension]))
        self.K = matrix(zeros([self.dimension, self.dimension]))
        self.A = matrix(zeros([self.dimension, self.dimension]))
        self.B = matrix(zeros([self.dimension]))
        self.C = matrix(zeros([self.dimension, self.dimension]))
        self.D = matrix(zeros([self.dimension, self.dimension]))


    """OBSERVER"""
    def get_est_state(self, y):
        L = control.acker(transpose(self.A), transpose(self.C), [0, 0])
        print(L)
        #L = scipy.signal.place_poles(transpose(self.A), transpose(self.C), [0.5, 0.5]).gain_matrix
        L = transpose(matrix(L))

        print('get state x_est: {}'.format(self.x_est))
        self.x_est = dot(self.A, self.x_est) + dot(self.B, self.u) +\
                         dot(L, (y-dot(self.C, self.x_est)))
        print('get state x_est: {}'.format(self.x_est))


    """CONTROLLER"""
    def get_control_signal(self, y):
        #K = -scipy.signal.place_poles(np.array(self.A), np.array(self.B), [0, 0]).gain_matrix
        K = -dot(np.linalg.pinv(self.B), self.A)
        self.get_est_state(y)
        self.u = dot(K, self.x_est)
        self.u  = self.u
        return self.u

    def set_dimension(self, dimension):
        self.dimension = dimension
        self.__zero_init()




dyn_process_session = DynamicProcessSession()
controller = Controller()
dyn_process_session.get_dimension()
dyn_process_session.set_dimension('2')
A = [[0.1, 0.2],[0.3, 0.4]]
B = [1, -1]
C = [0.6, 0.8]
D = [[0, 0],[0, 0]]
controller.A = matrix(A)
controller.B = matrix(B).transpose()
controller.C = matrix(C)
controller.D = matrix(D)
dyn_process_session.set_coefficient('A', json.dumps(A))
dyn_process_session.set_coefficient('B', json.dumps(B))
dyn_process_session.set_coefficient('C', json.dumps(C))
dyn_process_session.get_output()

while(True):
    print('------------------')
    y = dyn_process_session.get_output()
    print('y: {}'.format(y))
    y = matrix(y).transpose()
    u = controller.get_control_signal(y)
    dyn_process_session.set_input(np_to_json(u))
    time.sleep(1)


