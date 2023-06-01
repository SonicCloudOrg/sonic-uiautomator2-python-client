# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: resp_handler.py
# @Time : 2023/6/1 16:09
# @Email: lihuacai168@gmail.com


import json
from typing import Any, Dict, Optional, Union

import requests
from requests.exceptions import HTTPError

from common.http_client import HttpRequest
from models import BaseResp, ErrorMsg


class RespHandler:
    DEFAULT_REQUEST_TIMEOUT = 15000

    def __init__(self):
        self.request_timeout: int = self.DEFAULT_REQUEST_TIMEOUT

    def set_request_timeout(self, timeout: int) -> None:
        self.request_timeout = timeout

    def get_resp(self, http_request: HttpRequest, timeout: Optional[int] = None) -> BaseResp:
        timeout = timeout if timeout is not None else self.request_timeout
        try:
            response = http_request.send(timeout=timeout)
            return self.init_resp(response.text)
        except (HTTPError, requests.exceptions.RequestException) as e:
            print(e)
            raise Exception(e)

    @staticmethod
    def init_resp(response: str) -> BaseResp:
        response_dict: dict = json.loads(response)
        if "traceback" in response or "stacktrace" in response:
            response = response.replace("stacktrace", "traceback")
            return RespHandler.init_error_msg(response)
        else:
            return BaseResp(**response_dict)

    @staticmethod
    def init_header() -> Dict[str, str]:
        headers: Dict[str, str] = {"Content-Type": "application/json; charset=utf-8"}
        return headers

    @staticmethod
    def init_error_msg(resp: str) -> BaseResp:
        err_dict: dict = json.loads(resp)
        err = BaseResp(**err_dict)
        if 'value' in err_dict:
            error_msg_dict = err_dict.get('value', {})
            error_msg = ErrorMsg(**error_msg_dict)
            err.err = error_msg
        err.value = None
        return err
