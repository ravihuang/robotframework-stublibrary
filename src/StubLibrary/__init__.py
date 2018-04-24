#coding:utf-8
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
import psutil
import hashlib
from functools import wraps
from types import FunctionType
from decorator import decorator
from six.moves.urllib.parse import urlparse, urlencode
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import HTTPError
from robot.utils.asserts import assert_true, assert_false
from robot.api import logger
from allpairspy import AllPairs

from StubLibrary.http_stub import HTTP
from StubLibrary.sip_stub import SIP
from .robotlibcore import DynamicCore, keyword
__version__ = '0.1.5'

#给每个方法添加svr参数
def wrapper(method):
    @wraps(method)
    def wrapped(self,*args, **kwrds):
        if 'svr' in method.__code__.co_varnames:
            svr=method.__code__.co_varnames.index('svr')
            if args[svr]!=None:
                args[0].svr=args[svr]
        return method(*args, **kwrds)
    return decorator(wrapped,method)
class MetaClass(type):
    #装饰类中的每个方法
    def __new__(meta, classname, bases, classDict):
        newClassDict = {}
        for attributeName, attribute in classDict.items():
            if isinstance(attribute, FunctionType) and \
               not attribute.__name__.startswith('__'):
                attribute = wrapper(attribute)
            newClassDict[attributeName] = attribute
        return type.__new__(meta, classname, bases, newClassDict)

class StubLibrary(MetaClass("DynamicCore", (DynamicCore,), {})):
    """
    Stub Library contains utilities meant for Robot Framework's usage.
    This can allow you to stub a interface for your client test

    References:

     + abc - http://

    Notes:

    `compatible* - or at least theoretically it should be compatible. Currently tested only with win7`

    Example Usage:
    | # Setup |
    | Create Server | http://127.0.0.1
    | # Guard assertion (verify that test started in expected state). |
    | Add Response | /orders | json={"name":"iphone","quantity":123}
    | # Teardown |
    | Close All Server |
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    __SVRS__ = []
    __STUBS__={'http':HTTP, 'https':HTTP, 'sip':SIP}
  
    def __init__(self,*args):
        if not args:
            args=['http']
        l=[StubLibrary.__STUBS__[i]() for i in args]
        super(DynamicCore,self).__init__(l)
    
    @keyword
    def create_server(self,url='http://127.0.0.1',**kwargs):
        '''create server with url'''
        url=urlparse(url)
        stub=StubLibrary.__STUBS__.get(url.scheme.lower(),None)
        if stub is None:
            raise Exception("not support server: %s" % url.scheme)

        self.svr=stub().create_server(url,**kwargs)
        StubLibrary.__SVRS__.append(self.svr)
        return self.svr
    @keyword
    def get_all_servers(self):
        return StubLibrary.__SVRS__
    @keyword
    def add_response_to_server(self,svr=None,*args,**kwargs):
        self.svr.add_response(*args,**kwargs)
        
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
        for i in StubLibrary.__SVRS__:
            i.shutdown()
    @keyword
    def switch_server(self,svr):
        '''switch server'''
        self.svr=svr
    @keyword
    def should_call_1_time(self, method, url,svr=None,msg="should_call_1_time"):
        assert_true(self.svr.should_call_1_time(method, url),msg)
    @keyword
    def should_not_call(self, method, url,svr=None,msg=None):
        assert_true(self.svr.should_not_call(method, url),msg)
    @keyword
    def should_call_x_time(self, method, url,x,svr=None,msg="should_call_x_time"):
        assert_true(self.svr.should_call_x_time(method, url,x),msg)
    
    @staticmethod
    @keyword
    def create_testcases(parameters,rst,**kwargs):
        """
        Using parameters to create testcases by pairwise method
        
        Optionally, you can specify:
        filter_func - https://github.com/thombashi/allpairspy/blob/master/examples/example2.1.py 
        n - https://github.com/thombashi/allpairspy/blob/master/examples/example1.2.py
        previously_tested - https://github.com/thombashi/allpairspy/blob/master/examples/example1.3.py
        in kwargs to customize the generared testcases set
    
        Example usage:
        | ${l1}   | Create List |  1  |  2  |  3  |
        | ${l2}   | Create List |  a  |  b  |
        | ${l}    | Create List |  ${l1} |  ${l2}  |
        | ${x}    | Create Testcases | ${l} |
        | ${x}    | Create Testcases | ${l} |  n=1  |        
        """
        if kwargs.has_key('n'):
            kwargs['n']=int(kwargs['n'])
        rst+=list(AllPairs(parameters, **kwargs))
        return rst
    @staticmethod
    @keyword(name='MD5 Sum')
    def md5sum(fname):
        """
        Calculating digital fingerprint of a file's 128-bit MD5 hashes
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    @staticmethod
    @keyword
    def kill_process(name):
        """
        Kill Processes by name
        """
        for proc in psutil.process_iter():
            if proc.name() == name:                
                proc.kill()
                return True
        return False  
    @staticmethod
    @keyword
    def set_hosts(address,names,type='ipv4'):
        '''add item to system hosts file'''
        from python_hosts import Hosts, HostsEntry
        hosts = Hosts()
        if isinstance(names,str):
            names=[names]
        new_entry = HostsEntry(entry_type=type, address=address, names=names)    
        hosts.add([new_entry])
        hosts.write()
    @staticmethod
    @keyword
    def execute(expression, modules=None, namespace=None):
        if modules==u"None":
            modules=None
        from robot.libraries.BuiltIn import BuiltIn
        from robot.utils import is_string
        bi=BuiltIn()
        if is_string(expression) and '$' in expression:
            expression, variables = bi._handle_variables_in_expression(expression)
        else:
            variables = {}
        namespace = bi._create_evaluation_namespace(namespace, modules)
        try:
            if not is_string(expression):
                raise TypeError("Expression must be string, got %s."
                                    % type_name(expression))
            if not expression:
                raise ValueError("Expression cannot be empty.")
            exec(expression, namespace, variables)
        except:
            raise RuntimeError("Evaluating expression '%s' failed: %s"
                                   % (expression, "---"))