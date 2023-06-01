# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: models.py
# @Time : 2023/6/1 16:16
# @Email: lihuacai168@gmail.com

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional


@dataclass
class ErrorMsg:
    error: str
    message: str
    traceback: str


@dataclass
class BaseResp:
    session_id: str = ""
    err: Optional[ErrorMsg] = None
    value: Any = None


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
