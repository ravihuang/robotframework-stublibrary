import json
import re

class RequestedParams:
    def __init__(self, cookies, body, content_type,
                 files, headers, query_params):
        self.cookies = cookies
        self.body = body
        self.content_type = content_type
        self.files = files
        self.headers = headers
        self.query_params = query_params


class HeaderDoesNotExist:
    def __repr__(self):
        return "<HEADER DOES NOT EXIST>"


class Statistic:
    def __init__(self, method, url):
        self.method = method
        self.url = url
        self.requests= []
        self._current_request_index = None
        self._number_of_requests_not_specify = True
        self._error_messages = ["Expect that server was requested with [{0}] {1}.".format(method.upper(),url)]

    @property
    def requested_times(self):
        return len(self.requests)

    def exactly_once(self):
        return self.exactly_1_times()

    def exactly_twice(self):
        return self.exactly_2_times()

    def for_the_first_time(self):
        return self.for_the_1_time()

    def for_the_second_time(self):
        return self.for_the_2_time()

    def __getattr__(self, item):
        exactly_times_pattern = r"^exactly_(?P<number>\d+)_times$"
        exactly_times_result = re.match(exactly_times_pattern, item)
        if exactly_times_result:
            number = int(exactly_times_result.groupdict()["number"])
            return self._exactly_times(number)

        for_the_time_pattern = r"^for_the_(?P<number>\d+)_time$"
        for_the_time_result = re.match(for_the_time_pattern, item)
        if for_the_time_result:
            number = int(for_the_time_result.groupdict()["number"])
            return self._for_the_time(number)

        raise AttributeError("'Statistic' object has no attribute '{0}'".format(item))

    def _exactly_times(self, expected_requested_times):
        self._number_of_requests_not_specify = False
        if expected_requested_times != self.requested_times:
            self._error_messages.append(" {0} times.\nBut server was requested {0} times."
                                        .format(expected_requested_times,self.requested_times))
                                        
            self._raise_assertion()
        return lambda: self

    def _for_the_time(self, times):
        if self.requested_times < times:
            self._error_messages.append(
                " At least {0} times.\nBut server was requested {1} times."
                .format(times,self.requested_times))
            self._raise_assertion()
        else:
            self._current_request_index = times - 1
            return lambda: self

    def with_cookies(self, cookies):
        actual_cookies = self.get_current_request().cookies
        if cookies != actual_cookies:
            requested_time = self._current_request_index + 1
            self._error_messages.append("\nFor the {0} time: with cookies {1}.\nBut for the {0} time: cookies was {2}."
                                        .format(requested_time,cookies,actual_cookies))
        return self

    def with_body(self, body):
        actual_body = self.get_current_request().body.decode("utf-8", errors="skip")
        if body != actual_body:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
                "\nFor the {0} time: with body {1}.\nBut for the {0} time: body was {2}."
                .format(requested_time,body.__repr__(),actual_body.__repr__()))
        return self

    def with_json(self, json_dict):
        body = json.dumps(json_dict, sort_keys=True)

        actual_body = self.get_current_request().body.decode("utf-8", errors="skip")
        try:
            actual_json_dict = json.loads(actual_body)
        except json.JSONDecodeError:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
            "\nFor the {0} time: with json {1}.\nBut for the {0} time: json was corrupted {2}."
             .format(requested_time,body,actual_body.__repr__()))
            return self

        actual_body = json.dumps(actual_json_dict, sort_keys=True)
        if body != actual_body:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
                "\nFor the {0} time: with json {1}.\nBut for the {0} time: json was {2}."
                .format(requested_time,body,actual_body))
        return self

    def with_content_type(self, content_type):
        actual_content_type = self.get_current_request().content_type
        if content_type != actual_content_type:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
                "\nFor the {0} time: with content type {1}.\nBut for the {0} time: content type was {2}."
                .format(requested_time,content_type.__repr__(),actual_content_type.__repr__())
            )
        return self

    def with_files(self, files):
        actual_files = self.get_current_request().files
        if files != actual_files:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
                "\nFor the {0} time: with files {1}.\nBut for the {0} time: files was {2}."
            .format(requested_time,files,actual_files))
        return self

    def with_headers(self, headers):
        actual_headers = self.get_current_request().headers
        expected_headers = {name.upper(): value for name, value in headers.items()}

        headers_diff = self._get_headers_diff(expected_headers, actual_headers)
        if headers_diff:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
                "\nFor the {0} time: with headers contain {1}.\nBut for the {0} time: headers contained {2}."
            .format(requested_time,expected_headers,headers_diff))
        return self

    @staticmethod
    def _get_headers_diff(expected_headers, actual_headers):
        headers_diff = {}

        for header_name, header_value in expected_headers.items():
            if header_name in actual_headers and header_value != actual_headers[header_name]:
                headers_diff[header_name] = actual_headers[header_name]
            elif header_name not in actual_headers:
                headers_diff[header_name] = HeaderDoesNotExist()

        return headers_diff

    def with_query_params(self, query_params):
        actual_query_params = self.get_current_request().query_params

        if query_params != actual_query_params:
            requested_time = self._current_request_index + 1
            self._error_messages.append(
                "\nFor the {0} time: with query params {1}.\n"
                "But for the {0} time: query params was {2}."
            .format(requested_time,query_params,actual_query_params))

        return self

    def get_current_request(self):
        if self._current_request_index is None:
            raise AttributeError("You should specify concrete request for check with 'for_the_<any_number>_time'")
        return self.requests[self._current_request_index]

    def check(self):
        if not self.requested_times and self._number_of_requests_not_specify:
            self._error_messages.append("\nBut server was requested 0 times.")

        if self.errors_exist:
            self._raise_assertion()
        else:
            self._clean_state()
            return True

    @property
    def errors_exist(self):
        return len(self._error_messages) > 1

    def _raise_assertion(self):
        error_message = "".join(self._error_messages)
        self._clean_state()
        raise AssertionError(error_message)

    def _clean_state(self):
        self._error_messages = self._error_messages[0:1]
        self._number_of_requests_not_specify = True
        self._current_request_index = None