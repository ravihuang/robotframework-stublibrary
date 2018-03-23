"""
httpstub - http stub

"""
import sys
import webtest
import falcon
from webtest.http import StopableWSGIServer
from falcon_multipart.middleware import MultipartMiddleware
from .endpoint import Endpoint
from .statistic import Statistic, RequestedParams
from .robotlibcore import DynamicCore, keyword

class HTTP(falcon.API):
    """
    HTTP Protocol Stub
    """
    def __init__(self):
        super(HTTP,self).__init__(middleware=[MultipartMiddleware()]) 
        
    def set_url(url):
        self.req_options = self._get_request_options()
        self._host = url.hostname
        self._port = url.port if url.port else 80
        self._endpoints = {}
        self._statistics = {}
        self.add_sink(self._handle_all)
        self._server = StopableWSGIServer.create(self, host=self._host, port=self._port)

    @staticmethod
    def _get_request_options():
        options = falcon.RequestOptions()
        options.auto_parse_qs_csv = False
        return options
    
    def _handle_all(self, request, response):
        route = (request.method.lower(), self.base_uri + request.path.rstrip("/"))
        endpoint = self._endpoints.get(route, None)
        if endpoint:
            self._set_response_attributes_from_endpoint(response, endpoint)
            endpoint.called()
        else:
            error_endpoint = Endpoint(request.method, self.base_uri + request.path).once()
            error_endpoint.called()
            self._set_response_attributes_from_endpoint(response, error_endpoint)

        self._update_statistics(request, route)
        
    def _on_(self, method, url):
        new_endpoint = Endpoint(method.lower(), self.base_uri + url.rstrip("/"))
        self._endpoints[(new_endpoint.method, new_endpoint.url)] = new_endpoint
        return new_endpoint
    
    @staticmethod
    def _set_response_attributes_from_endpoint(response, endpoint):
        response.status = getattr(falcon, "HTTP_{0}".format(endpoint.status))
        response.body = endpoint.body
        if endpoint.content_type:
            response.content_type = endpoint.content_type
        for header_name, header_value in endpoint.headers.items():
            response.set_header(header_name, header_value)
        for cookie_name, cookie_value in endpoint.cookies.items():
            response.set_cookie(cookie_name, cookie_value)

    def _update_statistics(self, request, route):
        self._statistics.setdefault(route, Statistic(route[0], route[1]))
        statistic = self._statistics.get(route)
        statistic.requests.append(RequestedParams(cookies=request.cookies,
                                                  body=request.bounded_stream.read(),
                                                  content_type=request.content_type,
                                                  files=self._get_files(request),
                                                  headers=request.headers,
                                                  query_params=request.params))

    @staticmethod
    def _get_files(request):
        files = {
            param_name: param_value.file.read()
            for param_name, param_value in request.params.items()
            if hasattr(param_value, "file")
        }
        return files if files else None

    @property
    def base_uri(self):
        return "http://{0}:{1}".format(self._host,self._port)

    def clear(self):
        self._endpoints = {}
        self._statistics = {}
        
    def was_requested(self, method, url):
        route = (method.lower(), self.base_uri + url.rstrip("/"))
        self._statistics.setdefault(route, Statistic(route[0], route[1]))
        return self._statistics.get(route)

    def was_not_requested(self, method, url):
        route = (method.lower(), self.base_uri + url)
        self._statistics.setdefault(route, Statistic(route[0], route[1]))
        statistic = self._statistics.get(route)
        statistic.exactly_0_times()
        return statistic
    
    @keyword
    def add_response(self,method,path,status=200, body = None, content_type = None,
                 headers = None, cookies = None,
                 json = None):
        self._on_(method,path).response(status,body,content_type,headers,cookies,json)

    def _shutdown(self):
        self._server.shutdown()

    