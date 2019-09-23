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
        self.__address = 'http://20.0.0.2:5000/'

    def get_output(self):
        r = self.__session.get(self.__address + 'in_out')
        return json.loads(r.text)

    def set_input(self, value):
        r = self.__session.put(self.__address + 'in_out', data={'data':value})

    def get_coefficient(self, type):
        r = self.__session.get(self.__address + 'coefficients/' + type)
        print(r.text)

    def set_coefficient(self, type, value):
        r = self.__session.put(self.__address + 'coefficients/' + type,
                               data={'data':value})

    def get_num_states(self):
        r = self.__session.get(self.__address + 'num_states').json()
        print(r)

    def set_num_states(self, value):
        r = self.__session.put(self.__address + 'num_states',
                               data={'data': value})

class Controller():
    def __init__(self):
        self.num_states = 3
        self.num_inputs = 2
        self.__zero_init()

    def __zero_init(self):
        self.x_est = matrix(zeros([self.num_states])).transpose()
        self.u = matrix(zeros([self.num_inputs])).transpose()
        self.K = None
        self.A = None
        self.B = None
        self.C = None
        self.D = None


    """OBSERVER"""
    def get_est_state(self, y):
        self.x_est = dot(self.A, self.x_est) + dot(self.B, self.u) +\
                         dot(self.L, (y-dot(self.C, self.x_est)))
        print('get state x_est: {}'.format(self.x_est))


    """CONTROLLER"""
    def get_control_signal(self, y, feed_forward):
        self.get_est_state(y)
        self.u = dot(self.K, self.x_est)
        self.u  = self.u + dot(self.D, feed_forward)
        return self.u

    def set_num_states(self, num_states):
        self.num_states = num_states
        self.__zero_init()

    def calculate_observer_controller(self):
        #self.L = control.acker(transpose(self.A), transpose(self.C), [0, 0])
        self.L = dot(np.linalg.pinv(transpose(self.C)), transpose(self.A))
        self.L = transpose(matrix(self.L))
        self.K = -dot(np.linalg.pinv(self.B), self.A)


num_states = 3
feed_forward = 100
A = [[0.1, 0.2, 0.3],
     [0.3, 0.4, 0.1],
     [0.2, 0.7, 0.4]
    ]
B = [[1, 0.5],
     [-1, -0.3],
     [0.2, 0.1]
    ]
C = [[0.6, 0.8, 0.7],
     [0.5, 0.4, 0.2]
    ]
D = [1]
controller = Controller()
controller.set_num_states(num_states)
controller.A = matrix(A)
controller.B = matrix(B)
controller.C = matrix(C)
controller.D = matrix(D)
controller.calculate_observer_controller()
dyn_process_session = DynamicProcessSession()
dyn_process_session.set_num_states(str(num_states))
dyn_process_session.set_coefficient('A', json.dumps(A))
dyn_process_session.set_coefficient('B', json.dumps(B))
dyn_process_session.set_coefficient('C', json.dumps(C))

W_c = control.ctrb(controller.A, controller.B)
W_o = control.obsv(controller.A, controller.C)
print(np.linalg.matrix_rank(W_c))
print(np.linalg.matrix_rank(W_o))

t0 = time.perf_counter()
freq_counter = 0
freq = 0
while(True):
    freq_counter += 1
    t = time.perf_counter()
    if (t - t0) > 1:
        freq = freq_counter
        freq_counter = 0
        t0 = t
    print("freq: {}".format(freq))
    print('------------------')
    y = dyn_process_session.get_output()
    print('y: {}'.format(y))
    u = controller.get_control_signal(y, feed_forward)
    #print("sterowanie: {}".format(u))
    dyn_process_session.set_input(np_to_json(u))
    time.sleep(0.1)
    print("====================================")
#
###dyn_process_session = DynamicProcessSession()
###dyn_process_session.get_num_states()
###dyn_process_session.set_num_states(3)
###dyn_process_session.get_num_states()
###dyn_process_session.set_coefficient('A', json.dumps(A))
###dyn_process_session.get_coefficient('A')
###y = dyn_process_session.get_output()
###print(y)
###y = dyn_process_session.set_input(y)
