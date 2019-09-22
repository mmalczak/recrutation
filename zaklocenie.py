import requests
import json
import time


class DynamicProcessSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://20.0.0.2:8080/'

    def set_nonexistent(self, data):
        self.__session.put(self.__address + 'nonexistent/', 
			   data={'value':data})

    def get_output(self):
        r = self.__session.get(self.__address + 'in_out/')
        return json.loads(r.text)

    def set_input(self, value):
        r = self.__session.put(self.__address + 'in_out/', data={'value':value})

    def get_coefficient(self, type):
        r = self.__session.get(self.__address + 'coefficients/' + type + '/')
        print(r.text)

    def set_coefficient(self, type, value):
        r = self.__session.put(self.__address + 'coefficients/' + type + '/',
                               data={'value':value})

    def get_num_states(self):
        r = self.__session.get(self.__address + 'num_states/')
        print(r.text)

    def set_num_states(self, value):
        r = self.__session.put(self.__address + 'num_states/',
                               data={'value':value})

dyn_process_session = DynamicProcessSession()
data = "11100010"
#data = 10000*data
data = '[' + data + '], '
last_data = '[' + data + ']'
while(True):
#    dyn_process_session.set_nonexistent(data)
    dyn_process_session.set_input("[[1000000.03532324], [2]]") 
#    dyn_process_session.set_input("[[bleble.03532324], " + 
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    data +
#                                    last_data +
#                                    ']')
#                                    
                            
                                                        #['a']]")
							#[1000000.03532324]])))
    print(time.perf_counter())
