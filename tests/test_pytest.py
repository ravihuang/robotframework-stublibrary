#coding:utf-8
from StubLibrary import StubLibrary as x
import os
import requests

stub=None
def setup_function(function):
    global stub
    stub = x()

def teardown_function(function):    
    stub.close_all_server()
    import time
    #time.sleep(20)

def test_http():
    svr=stub.create_server("http://0.0.0.0:8123")
    svr.add_response("get", "/hello",status=200, 
                     body="Hello, World!")
    svr.add_response("get", "/things",status=201, 
                     json='''{"name":"iphone","quantity":123}''', content_type="text/plain")  
    
    response = requests.get("http://127.0.0.1:8123/hello")
    
    response1 = requests.get("http://127.0.0.1:8123/things")
    assert 200==response.status_code
    assert "Hello, World!"==response.content
    assert response.headers.get("content-type")=='application/json; charset=UTF-8'    
    assert response1.json()=={"name":"iphone","quantity":123}
    
    import json
    d=json.loads(response1.content)    
    assert d=={"name":"iphone","quantity":123}    
  
    assert svr.should_call_1_time("get","/hello")
    assert svr.should_not_call("get","/helloa")
    assert svr.should_call_x_time("get","/hello",1)
    response = requests.get("http://127.0.0.1:8123/hello")
    assert svr.should_call_x_time("get","/hello",2)

def test_http_cn():    
    s1=  stub.create_server("http://0.0.0.0:8123")
    s2 = stub.create_server("http://0.0.0.0:6123")
    stub.add_response_to_server(s1,"get", "/hello",status=200, 
                     body="Hello, World!")
    stub.add_response("get", "/things",status=200, 
                     json='{"name":"苹果","quantity":123}', content_type="application/json;charset=utf-8")  
    response = requests.get("http://127.0.0.1:8123/hello")    
    response1 = requests.get("http://127.0.0.1:8123/things")
    assert response.content=='Hello, World!'
    assert response1.content=='{"name": "苹果", "quantity": 123}',response1.content

# 用于调试
#def test_execute():
    #from robot import run_cli
    #run_cli(['--test', 'case-execute', 'hellosuite.txt'])
#def test_https_bin():
    #r2=requests.get("http://192.168.117.156/mt/orders")
    #response = requests.get("https://httpbin.org/get",cert="client_certs/client.pem")
    #print response.status_code,response.content
    #print("Done!")
