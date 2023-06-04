# !/usr/bin/python3
# -*- coding: utf-8 -*-
from dataclasses import dataclass
from enum import StrEnum
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


class Method(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class PasteboardType(StrEnum):
    PLAIN_TEXT = "plaintext"
    IMAGE = "image"
    URL = "url"


class AndroidSelector(StrEnum):
    CLASS_NAME = "class name"
    Id = "id"
    ACCESSIBILITY_ID = "accessibility id"
    XPATH = "xpath"
    UIAUTOMATOR = "-android uiautomator"


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
