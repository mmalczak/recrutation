import requests
import json
import time
import numpy as np
import scipy.signal
import control

def np_to_json(data):
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
        return json.loads(r.text)
        #print(r.text)

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
        self.x_est = np.matrix(np.zeros([self.dimension])).transpose()
        self.u = np.matrix(np.zeros([self.dimension]))
        self.K = np.matrix(np.zeros([self.dimension, self.dimension]))
        self.A = np.matrix([[0, 0],[0, 0]])
        self.B = np.matrix([[0, 0],[0, 0]])
        self.C = np.matrix([[0, 0],[0, 0]])
        self.D = np.matrix([[0, 0],[0, 0]])


    """OBSERVER"""
    def get_est_state(self, y):
        L = scipy.signal.place_poles(np.transpose(self.A), np.transpose(self.C), [0, 0]).gain_matrix
        L = np.matrix(L).transpose()
        #sys = control.ss(self.A, self.B, self.C, self.D, True)
        #gram = control.gram(sys, 'o')
        np.dot(self.B, self.u)
        x_est = np.dot(self.A, self.x_est) + np.dot(self.B, self.u) +\
                        np.dot(L, (y-np.dot(self.C, self.x_est)))
        self.x_est = x_est
        print('x_est: {}'.format(self.x_est))

    """CONTROLLER"""
    def get_control_signal(self, y):
        #K = -scipy.signal.place_poles(np.array(self.A), np.array(self.B), [0, 0]).gain_matrix
        K = -np.dot(np.linalg.pinv(self.B), self.A)
        self.get_est_state(y)
        self.u = np.dot(K, self.x_est)
        #self.u = np.dot(K, y)
        return self.u 

    def set_dimension(self, dimension):
        self.dimension = dimension
        self.__zero_init()




dyn_process_session = DynamicProcessSession()
controller = Controller()
dyn_process_session.get_dimension()
dyn_process_session.set_dimension('2')
A = [[1, 2],[2, 4]]
B = [1, -1]
C = [[1, 0],[0, 1]]
D = [[0, 0],[0, 0]]
dyn_process_session.set_coefficient('A', json.dumps(A))
controller.A = np.matrix(A)
controller.B = np.matrix(B).transpose()
controller.C = np.matrix(C)
controller.D = np.matrix(D)
dyn_process_session.set_coefficient('GAMMA', json.dumps(B))
dyn_process_session.set_coefficient('C', json.dumps(C))
dyn_process_session.get_output()

while(True):
    print('------------------')
    y = dyn_process_session.get_output()
    print('y: {}'.format(y))
    y = np.matrix(y).transpose()
    u = controller.get_control_signal(y)
    dyn_process_session.set_input(np_to_json(u))
    time.sleep(1)


