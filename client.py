import requests
import json
import time
import numpy as np


def np_to_json(data):
        return json.dumps(data.tolist())

def json_to_np(data):
    return np.array(json.loads(data))


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
        self.K = np.zeros([self.dimension, self.dimension]),

    """OBSERVER"""
    def get_est_state(self, y):
        return y

    """CONTROLLER"""
    def get_control_signal(self, y):
        x_est = self.get_est_state(y)
        return np.dot(self.K, x_est)

    def get_value(self):
        return self.__y

    def set_dimension(self, dimension):
        self.dimension = dimension
        self.__zero_init()




dyn_process_session = DynamicProcessSession()
controller = Controller()
dyn_process_session.get_dimension()
dyn_process_session.set_dimension('2')
dyn_process_session.set_coefficient('A', json.dumps([[1, 2],[2, 1]]))
dyn_process_session.get_coefficient('A')
dyn_process_session.set_coefficient('GAMMA', json.dumps([[1, 1],[1, 1]]))
dyn_process_session.set_coefficient('C', json.dumps([[1, 0],[0, 1]]))
dyn_process_session.get_output()

while(True):
    y = dyn_process_session.get_output()
    print(y)

    u = controller.get_control_signal(y)
    print(u)
    u = np.array([1, 2])
    dyn_process_session.set_input(np_to_json(u))
    time.sleep(1)


