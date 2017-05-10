#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import cherrypy

class Root(object):
    @cherrypy.expose
    def index(self):
        return "hello world"

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_port': 5000,
        'tools.proxy.on': True,
        'tools.proxy.base': '127.0.0.1'
    })
    cherrypy.quickstart(Root())
