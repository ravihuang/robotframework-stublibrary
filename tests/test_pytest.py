#coding:utf-8
from StubLibrary import StubLibrary as x
import os,urlparse
import requests

def test_https():
    svr = x().create_server("https://0.0.0.0:8123",keyfile='server.key',
                            certfile='server.cert',server_side=True)
    svr.add_response("get", "/hello",status=200, 
                     body="Hello, World!")
    svr.add_response("get", "/things",status=201, 
                     body="Two things awe me most!", content_type="text/plain")  

    response = requests.get("https://127.0.0.1:8123/hello"
                            ,cert=("server.cert",'server.key'),verify=False,
                            )
    print response.status_code,response.content    


def test_http():
    svr = x().create_server("http://0.0.0.0:8123",)
    svr.add_response("get", "/hello",status=200, 
                     body="Hello, World!")
    svr.add_response("get", "/things",status=201, 
                     json='''{"name":"iphone","quantity":123}''', content_type="text/plain")  
    
    response = requests.get("http://127.0.0.1:8123/hello")
    
    response1 = requests.get("http://192.168.117.1:8123/things")
    print response.status_code,response.content,response.headers
    import json
    print response1.status_code,response1.content
    d=json.loads(response1.content)
    print d
    a,b=svr.was_requested("get","/hello"),svr.was_requested("get","/things")
    print svr.should_call_1_time("get","/hello")
    print svr.should_not_call("get","/helloa")
    print svr.should_call_x_time("get","/hello",1)
    response = requests.get("http://127.0.0.1:8123/hello")
    print svr.should_call_x_time("get","/hello",2)

def test_http_cn():
    xx = x()
    s1=  xx.create_server("http://0.0.0.0:8123")
    s2 = xx.create_server("http://0.0.0.0:6123")
    xx.add_response_to_server(s1,"get", "/hello",status=200, 
                     body="Hello, World!")
    xx.add_response("get", "/things",status=200, 
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
