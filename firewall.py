import random
import string
import cherrypy
import json
import os


@cherrypy.expose
class FirewallWebService(object):

    def PUT(self, value):
        os.system('iptables -A FORWARD -s ' + value + ' -j DROP') 

if __name__ == '__main__':
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        }
    }
    cherrypy.server.socket_host = '40.0.0.99'
    cherrypy.tree.mount(FirewallWebService(), '/blocked_IPs/', conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
