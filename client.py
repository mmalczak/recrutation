import requests

class DynamicProcessSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://20.0.0.2:8080/'

    def get_output(self):
        r = self.__session.get(self.__address + 'in_out/')
        print(r.text)

    def set_input(self, data):
        r = self.__session.put(self.__address + 'in_out/', data=data)
        print(r.text)


dyn_process_session = DynamicProcessSession()
dyn_process_session.get_output()
dyn_process_session.set_input({'value':'1 2'})
