import sys
import requests
import json
import time
import numpy as np
import queue
from numpy import matrix
from numpy import dot
from numpy import zeros
from numpy import transpose
import scipy.signal
import control
from commands import Commands
from commands import CommandsThread
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
        return data

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

    def get_num_outputs(self):
        data = self.__get('num_outputs')
        return data

    def set_num_outputs(self, value):
        r = self.__put('num_outputs', value)

    def get_delay(self):
        data = self.__get('delay')
        return data

    def set_delay(self, value):
        r = self.__put('delay', value)


class Controller():
    def __init__(self, num_states, num_inputs):
        self.num_states = num_states
        self.num_inputs = num_inputs
        self.__zero_init()
        self.update_shapes()

    def update_shapes(self):
        self.expected_shapes = {'A':(self.num_states, self.num_states),
                                'B':(self.num_states, self.num_inputs),
                                'C':(self.num_inputs, self.num_states),
                                'D':(self.num_inputs, self.num_inputs),
                                'L':(self.num_states, self.num_inputs),
                                'K':(self.num_inputs, self.num_states)
                                }

    def __zero_init(self):
        self.x_est = matrix(zeros([self.num_states])).transpose()
        self.u = matrix(zeros([self.num_inputs])).transpose()
        self.K = None
        self.L = None
        self.A = None
        self.B = None
        self.C = None
        self.D = None

    def set_matrix(self, name, value):
        if type(value) is str:
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                logger.error("Wrong input data")
                return
        value = matrix(value)
        try:
            assert value.shape == self.expected_shapes[name]
        except AssertionError:
            logger.warning("Wrong matrix shape")
            return
        setattr(self, name, value)
        if name in ['A', 'B', 'C']:
            try:
                self.calculate_observer_controller()
            except TypeError:
                pass # one of the matrices could be not initialized

    """OBSERVER"""
    def get_est_state(self, y):
        self.x_est = dot(self.A, self.x_est) + dot(self.B, self.u) +\
                         dot(self.L, (y-dot(self.C, self.x_est)))
#        print('get state x_est: {}'.format(self.x_est))


    """CONTROLLER"""
    def get_control_signal(self, y, feed_forward):
        self.get_est_state(y)
        self.u = dot(self.K, self.x_est)
        self.u  = self.u + dot(self.D, feed_forward)
        return self.u

    def set_num_states(self, num_states):
        self.num_states = num_states
        self.__zero_init()
        self.update_shapes()

    def set_num_inputs(self, num_inputs):
        self.num_inputs = num_inputs
        self.__zero_init()
        self.update_shapes()

    def calculate_observer_controller(self):
        #self.L = control.acker(transpose(self.A), transpose(self.C), [0, 0])
        self.L = dot(np.linalg.pinv(transpose(self.C)), transpose(self.A)) # observer
        self.L = transpose(matrix(self.L))
        self.K = -dot(np.linalg.pinv(self.B), self.A) # controller

def main():
    queue_ = queue.Queue()
    commands = Commands(logger, queue_)
    commands_thread = CommandsThread(commands)
    commands_thread.start()

    num_states = 3
    num_inputs = 2
    delay = 0
    feed_forward = [[100],
                    [100]]
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
    D = [[1, 0], [0, 1]]
    controller = Controller(num_states, num_inputs)
    controller.set_matrix('A', A)
    controller.set_matrix('B', B)
    controller.set_matrix('C', C)
    controller.set_matrix('D', D)
    controller.calculate_observer_controller()

    dyn_process_session = DynamicProcessSession()
    dyn_process_session.set_num_states(json.dumps(num_states))
    dyn_process_session.set_num_outputs(json.dumps(num_inputs))
    dyn_process_session.set_delay(json.dumps(delay))
    dyn_process_session.set_coefficient('A', json.dumps(A))
    dyn_process_session.set_coefficient('B', json.dumps(B))
    dyn_process_session.set_coefficient('C', json.dumps(C))

    W_c = control.ctrb(controller.A, controller.B)
    W_o = control.obsv(controller.A, controller.C)
    print('The rank of controlability matrix is: {}'.format(
                                                np.linalg.matrix_rank(W_c)))
    print('The rank of observability matrix is: {}'.format(
                                                np.linalg.matrix_rank(W_o)))

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
        logger.info("freq: {}".format(freq))
        logger.info('------------------')
        y = dyn_process_session.get_output()
        y = json_to_np(y)
        logger.info('y: {}'.format(y))
        u = controller.get_control_signal(y, feed_forward)
        #print("sterowanie: {}".format(u))
        dyn_process_session.set_input(np_to_json(u))
        time.sleep(0.1)
        logger.info("====================================")
        try:
            [type, name, values] = queue_.get_nowait()
            getattr(controller, type)(name, values)
        except queue.Empty:
            pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
