#  Copyright (c) 2010 Franz Allan Valencia See
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import os
from six.moves.urllib.parse import urlparse, urlencode
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import HTTPError

from StubLibrary.http_stub import HTTP
from StubLibrary.commons import Commons
from .robotlibcore import DynamicCore, keyword
from robot.utils.asserts import assert_true, assert_false

__version__ = '0.1.4'

class StubLibrary(DynamicCore):
    """
    Stub Library contains utilities meant for Robot Framework's usage.

    This can allow you to stub a interface for your client test


    References:

     + abc - http://

    Notes:

    `compatible* - or at least theoretically it should be compatible. Currently tested only with win7`

    Example Usage:
    | # Setup |
    | Create Server | http://127.0.0.1/if
    | # Guard assertion (verify that test started in expected state). |
    | Add Route | /orders | {"name":"iphone","quantity":123}
    | # Teardown |
    | Close Server |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    __servers = []
    __STUBS={'http':HTTP,'https':HTTP}
    
    def __init__(self):
        libraries = [
            Commons()
        ]
        DynamicCore.__init__(self, libraries)
        
    @keyword
    def create_server(self,url='http://127.0.0.1',**kwargs):
        '''create server with url'''
        url=urlparse(url)
        stub=StubLibrary.__STUBS.get(url.scheme.lower(),None)
        if stub is None:
            raise Exception("not support server: %s" % url.scheme)

        self.svr=stub().create_server(url,**kwargs)
        StubLibrary.__servers.append(self.svr)
        return self.svr
    @keyword
    def get_all_servers(self):
        return StubLibrary.__servers
    @keyword
    def add_response(self,*args,**kwargs):
        self.svr.add_response(*args,**kwargs)
    
    @keyword
    def close_server(self):
        '''close current server'''
        self.svr.shutdown()
        
    @keyword
    def close_all_server(self):
        '''close all server'''
        for i in StubLibrary.__servers:
            i.shutdown()
    @keyword
    def switch_server(self,svr):
        '''switch server'''
        self.svr=svr
    @keyword
    def should_call_1_time(self, method, url,msg=None,svr=None):
        tmp=svr if svr else self.svr
        assert_true(tmp.should_call_1_time(method, url),msg)
    @keyword
    def should_not_call(self, method, url,msg=None,svr=None):
        tmp=svr if svr else self.svr
        assert_true(tmp.should_not_call(method, url),msg)
    @keyword
    def should_call_x_time(self, method, url,x,msg=None,svr=None):
        tmp=svr if svr else self.svr
        assert_true(tmp.should_call_x_time(method, url,x),msg)