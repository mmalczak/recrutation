import requests
import json
import time


class DynamicProcessSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://20.0.0.2:5000/'

    def set_input(self, value):
        r = self.__session.post(self.__address + 'in_out', data={'data':value})

    def set_nonexistent(self, value):
        r = self.__session.put(self.__address + 'nonexistent', data={'data':value})



dyn_process_session = DynamicProcessSession()
data = "11100010"
#data = 10000*data
data = '[' + data + '], '
last_data = '[' + data + ']'
while(True):
#    dyn_process_session.set_nonexistent(data)
    dyn_process_session.set_input("[[1000000.03532324]]")
    dyn_process_session.set_input("[[1000000.03532324], [2]]")
    dyn_process_session.set_input("[[1000000.03532324], [2], [30]]")
    dyn_process_session.set_input("[[1000000.03532324], [2], [213],\
                                    [23]]")
    dyn_process_session.set_input("[[1000000.03532324], [2], [213],\
                                    [23], [4324]]")
    dyn_process_session.set_nonexistent("[[1000000.03532324], [2]]")
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
