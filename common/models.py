# !/usr/bin/python3
# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass
from enum import StrEnum
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
        return BaseResp.value.get("sessionId")

class Method(StrEnum):
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

    @staticmethod
    def parse(value: object):
        se = json.loads(str(value))
        Capabilities.device = se["device"]
        Capabilities.browser_name = se["browserName"]
        Capabilities.sdk_version = se["sdkVersion"]
        Capabilities.cf_bundle_identifier = se["cfBundleIdentifier"]
        return Capabilities


@dataclass
class SessionInfo:
    session_id: str
    capabilities: Capabilities

    def __str__(self):
        return f"SessionInfo(session_id={self.session_id}, capabilities={self.capabilities})"

    @staticmethod
    def parse(value: object):
        se = json.loads(str(value))
        SessionInfo.session_id = se["sessionId"]
        SessionInfo.capabilities = Capabilities.parse(se["capabilities"])
        return SessionInfo


@dataclass
class WindowSize:
    width: int
    height: int

    def __str__(self):
        return f"WindowSize(width={self.width}, height={self.height})"


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
