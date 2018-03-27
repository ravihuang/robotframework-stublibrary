# coding:utf-8
import os,psutil 
import hashlib
from .robotlibcore import keyword
from allpairspy import AllPairs

class Commons(object):
    @keyword
    def create_testcases(self,parameters,**kwargs):
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
        l=list(AllPairs(parameters, **kwargs))
        return l
    
    @keyword(name='MD5 Sum')
    def md5sum(self,fname):
        """
        Calculating digital fingerprint of a file's 128-bit MD5 hashes
        """
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    @keyword
    def kill_process(self,name):
        """
        Kill Processes by name
        """
        for proc in psutil.process_iter():
            if proc.name() == name:                
                proc.kill()
                return True
        return False        
    @keyword
    def set_hosts(self,address,names,type='ipv4'):
        '''add item to system hosts file'''
        from python_hosts import Hosts, HostsEntry
        hosts = Hosts()
        if isinstance(names,str):
            names=[names]
        new_entry = HostsEntry(entry_type=type, address=address, names=names)    
        hosts.add([new_entry])
        hosts.write()        