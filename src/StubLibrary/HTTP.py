"""
httpstub - http stub

"""

__author__ = 'ravi.huang@gmail.com'
__version__ = '0.1'

import sys
import webtest
import falcon
from py_fake_server.server import FakeServer

class HTTP(object):
    """
    HTTP Protocol Stub
    """    
    def __init__(self,url):
        self.server=FakeServer(host=url.hostname, port=url.port)
        self.basepath=url.path
        self.server.start()
    
    def create_route(self,method,path):
        self.currresp=self.server.on_(method,path)        

    def set_response(self, status: int, body: Optional[str] = None, content_type: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None, cookies: Optional[Dict[str, str]] = None,
                 json: Optional[Dict] = None):
        self.currresp.response(status,body,content_type,headers,cookies,json)

    def shutdown(self):
        pass

    