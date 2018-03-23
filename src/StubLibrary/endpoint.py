import re
import json as json_lib

class Endpoint:
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self._statuses = []
        self._bodies = []
        self._content_types = []
        self._headers_list = []
        self._cookies_list = []
        self._called_times = 0
        self._last_endpoint_call_limited = False

    @property
    def status(self):
        return self._statuses[self._current_data_index]

    @property
    def body(self):
        return self._bodies[self._current_data_index]

    @property
    def content_type(self):
        return self._content_types[self._current_data_index]

    @property
    def headers(self):
        return self._headers_list[self._current_data_index]

    @property
    def cookies(self):
        return self._cookies_list[self._current_data_index]

    @property
    def _current_data_index(self):
        if self._called_times > len(self._statuses) - 1:
            return len(self._statuses) - 1
        return self._called_times

    def response(self, status, body = None, content_type = None,
                 headers = None, cookies = None,
                 json = None):
        if status == 204 and body is not None:
            raise AttributeError("status == 204 and body != None in one response")

        headers_names = [k.lower() for k in headers.keys()] if headers else []
        if content_type and "content-type" in headers_names:
            raise AttributeError("Explicit Content-Type and Content-Type in headers in one response")
        if cookies and "cookies" in headers_names:
            raise AttributeError("Explicit Cookies and Cookies in headers in one response")
        if body is not None and json is not None:
            raise AttributeError("'body' and 'json' in one response")

        if self._last_endpoint_call_limited:
            self._statuses.pop()
            self._bodies.pop()
            self._content_types.pop()
            self._headers_list.pop()
            self._cookies_list.pop()
            self._last_endpoint_call_limited = False

        if json is not None:
            content_type = content_type or "application/json"
            body = json_lib.dumps(json)

        self._append_data(status=status, body=body, content_type=content_type, headers=headers, cookies=cookies)
        return self

    def then(self):
        return self

    def called(self):
        self._called_times += 1

    def once(self):
        return self._1_times()

    def twice(self):
        return self._2_times()

    def __getattr__(self, item):
        times_pattern = r"^_(?P<number>\d+)_times$"
        regex_result = re.match(times_pattern, item)
        if regex_result:
            number = int(regex_result.groupdict()["number"])
            return self._times(number)
        raise AttributeError("'Endpoint' object has no attribute '{0}'".format(item))

    def _times(self, number):
        def times():
            for i in range(number - 1):
                self._append_data(status=self._statuses[-1], body=self._bodies[-1],
                                  content_type=self._content_types[-1], headers=self._headers_list[-1],
                                  cookies=self._cookies_list[-1])

            self._last_endpoint_call_limited = True
            self._append_data(status=500, body="Server has not responses for [{0}] {1}".format(self.method.upper(),self.url),
                              content_type="text/plain", headers={}, cookies={})
            return self

        return times

    def _append_data(self, status, body, content_type, headers, cookies):
        self._statuses.append(status)
        self._bodies.append(body)
        self._content_types.append(content_type)
        self._headers_list.append(headers or {})
        self._cookies_list.append(cookies or {})