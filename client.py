import requests
import json

class DynamicProcessSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://20.0.0.2:8080/'
        self.__dimension = 2

    def get_output(self):
        r = self.__session.get(self.__address + 'in_out/')
        print(r.text)

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



dyn_process_session = DynamicProcessSession()
dyn_process_session.get_dimension()
dyn_process_session.set_dimension('2')
dyn_process_session.set_coefficient('A', json.dumps([[1, 2],[2, 1]]))
dyn_process_session.get_coefficient('A')
dyn_process_session.set_coefficient('GAMMA', json.dumps([[1, 1],[1, 1]]))
dyn_process_session.set_coefficient('C', json.dumps([[1, 0],[0, 1]]))
dyn_process_session.get_output()
dyn_process_session.set_input('1 2')

