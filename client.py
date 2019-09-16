import requests

class DynamicProcessInOutSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://20.0.0.2:8080/in_out/'

    def get(self):
        r = self.__session.get(self.__address)
        print(r.text)

    def put(self, data):
        r = self.__session.put(self.__address, data=data)
        print(r.text)


dyn_process_in_out_session = DynamicProcessInOutSession()
dyn_process_in_out_session.get()
dyn_process_in_out_session.put({'value':'12'})
