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

import os,urlparse

from StubLibrary.http import HTTP
from StubLibrary.commons import Commons

__version_file_path__ = os.path.join(os.path.dirname(__file__), 'VERSION')
__version__ = open(__version_file_path__, 'r').read().strip()


class StubLibrary(Commons):
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
    __STUBS={'http':HTTP}
    
    def create_server(self,url='http://127.0.0.1'):
        url=urlparse.urlparse(url)
         
        stub=StubLibrary.__STUBS.get(url.scheme.lower(),None)
        if stub is None:
            raise Exception("not support server: %s" % url.scheme)

        self.svr=stub(url)
        StubLibrary.__servers.append(self.svr)

        return self.svr

    def create_route(self,method,path):
        return self.svr.create_route(method,path)    

    def set_response(self, status: int, body: Optional[str] = None, content_type: Optional[str] = None,
                 headers: Optional[Dict[str, str]] = None, cookies: Optional[Dict[str, str]] = None,
                 json: Optional[Dict] = None):
        self.svr.set_response(status,body,content_type,headers,cookies,json)

    def close_server(self):
        self.svr.shutdown()
        
    def close_all_server(self,svr):
        for i in StubLibrary.__servers:
            i.shutdown()
            
    def switch_server(self,svr):
        self.svr=svr    
