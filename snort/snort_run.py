from subprocess import Popen, PIPE, STDOUT
import requests
import pymongo


class FirewallSession():

    def __init__(self):
        self.__session = requests.Session()
        self.__address = 'http://40.0.0.99:8080/'

    def block_IP(self, value):
        r = self.__session.put(self.__address + 'blocked_IPs/', data={'value':value})


firewall_session = FirewallSession()

mongo_client = pymongo.MongoClient("mongodb://milosz:milosz@40.0.0.3/snort_db")


snort_process = Popen(['snort', '-dev', '-i', 'enp0s8',
                       '-c', '/etc/snort/snort.conf', '-A', 'console'],
                      stdout=PIPE, stderr=STDOUT, bufsize=1,
                      universal_newlines=True, close_fds=True)

with snort_process.stdout:
    for line in iter(snort_process.stdout.readline, ''):
        if 'Possible TCP DoS' in line:
            elements = line.split()
            if '{TCP}' in elements:
                pos = elements.index('{TCP}') + 1
                ip = elements[pos]
                ip = ip.split(':')[0]
                ip = ip + '/32'
#                ip = ip.split('.')
#                ip = ip[0] + '.' + ip[1] + '.' + ip[2] + '.' + '0/24'
                firewall_session.block_IP(ip)
                print(ip)
                print(line, end='')
                mongo_client.snort_db.blocked_addresses.insert_one({'ip':ip,
                    'reason': 'Possible TCP DoS - 400 messages during 3 seconds'})
rc = snort_process.wait()
