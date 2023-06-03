# !/usr/bin/python3
# -*- coding: utf-8 -*-

import json

import requests
from requests import Response

from common.models import BaseResp, ErrorMsg, Method


class HttpRequest:

    def __init__(self, method: Method, url: str, headers=None, params=None, body=None):
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self._body = body

    def body(self, body):
        self._body = json.loads(body) if isinstance(body, str) else body
        return self

    def send(self, timeout) -> Response:
        return HttpUtil.create_request(self.method, self.url,  timeout, self.headers, self.params, self._body)


class HttpUtil:

    @staticmethod
    def create_get(url: str, headers=None, params=None) -> HttpRequest:
        return HttpRequest(Method.GET, url, headers, params)

    @staticmethod
    def create_post(url: str, headers=None) -> HttpRequest:
        return HttpRequest(Method.POST, url, headers)

    @staticmethod
    def create_put(url: str, headers=None) -> HttpRequest:
        return HttpRequest(Method.PUT, url, headers)

    @staticmethod
    def create_delete(url: str, headers=None) -> HttpRequest:
        return HttpRequest(Method.DELETE, url, headers)

    @staticmethod
    def create_patch(url: str, headers=None) -> HttpRequest:
        return HttpRequest(Method.PATCH, url, headers)

    @staticmethod
    def create_request(method: Method, url: str, timeout: float, headers=None, params=None, body=None) -> Response:
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        if isinstance(body, str):
            body = json.loads(body)

        response = requests.request(method.value, url, timeout=timeout, headers=headers, params=params, data=json.dumps(body))
        return response

    # @staticmethod
    # def _handle_response(response: requests.Response) -> BaseResp:
    #     if response.status_code >= 400:
    #         err = ErrorMsg(error=str(response.status_code), message=response.text, traceback="")
    #     else:
    #         err = None
    #     try:
    #         value = response.json()
    #     except ValueError:
    #         value = response.text
    #     return BaseResp(session_id="", err=err, value=value)
