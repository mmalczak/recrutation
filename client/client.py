import sys
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
import logging.config
from logging_conf import DEFAULT_CONFIG
logging.config.dictConfig(DEFAULT_CONFIG)
logger = logging.getLogger(__name__)



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

    def __get(self, path):
        try:
            data = self.__session.get(self.__address + path).json()
            return data
        except ConnectionRefusedError:
            logger.critical('Connection refused when exectuting get on ' + path)
            sys.exit()
        except requests.exceptions.ConnectionError:
            logger.critical('Connection refused when exectuting get on ' + path)
            sys.exit()

    def __put(self, path, data):
        try:
            self.__session.put(self.__address + path, data={'data':data}).json()
        except ConnectionRefusedError:
            logger.critical('Connection refused when exectuting get on ' + path)
            sys.exit()
        except requests.exceptions.ConnectionError:
            logger.critical('Connection refused when exectuting get on ' + path)
            sys.exit()

    def get_output(self):
        data = self.__get('in_out')
        return json_to_np(data)

    def set_input(self, value):
        self.__put('in_out', value)

    def get_coefficient(self, type):
        data = self.__get('coefficients/' + type)
        return data

    def set_coefficient(self, type, value):
        r = self.__put('coefficients/' + type, value)

    def get_num_states(self):
        data = self.__get('num_states')
        return data

    def set_num_states(self, value):
        r = self.__put('num_states', value)


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
        self.L = dot(np.linalg.pinv(transpose(self.C)), transpose(self.A)) # observer
        self.L = transpose(matrix(self.L))
        self.K = -dot(np.linalg.pinv(self.B), self.A) # controller



def main():
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

    #dyn_process_session = DynamicProcessSession()
    #print(dyn_process_session.get_num_states())
    #dyn_process_session.set_num_states(3)
    #dyn_process_session.get_num_states()
    #dyn_process_session.set_coefficient('A', json.dumps(A))
    #print(dyn_process_session.get_coefficient('A'))
    #y = dyn_process_session.get_output()
    #print(y)
    #y = dyn_process_session.set_input(y)

if __name__ == '__main__':
    main()
