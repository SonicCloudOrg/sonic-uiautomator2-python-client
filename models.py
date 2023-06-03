# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


@dataclass
class ErrorMsg:
    error: str
    message: str
    traceback: str

    @staticmethod
    def get_message():
        return ErrorMsg.message


@dataclass
class BaseResp:
    session_id: str = ""
    err: Optional[ErrorMsg] = None
    value: Any = None

    @staticmethod
    def get_err():
        return BaseResp.err

    @staticmethod
    def get_value():
        return BaseResp.value

    @staticmethod
    def get_session_id():
        return BaseResp.session_id


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


@dataclass
class Capabilities:
    device: str
    browser_name: str
    sdk_version: str
    cf_bundle_identifier: str


@dataclass
class SessionInfo:
    session_id: str
    capabilities: Capabilities

    def __str__(self):
        return f"SessionInfo(session_id={self.session_id}, capabilities={self.capabilities})"


@dataclass
class WindowSize:
    width: int
    height: int


@dataclass
class ElementRect:
    x: int
    y: int
    width: int
    height: int

    @dataclass
    class IOSRectCenter:
        x: int
        y: int

    def get_center(self) -> "ElementRect.IOSRectCenter":
        return self.IOSRectCenter(self.x // 2, self.y // 2)
