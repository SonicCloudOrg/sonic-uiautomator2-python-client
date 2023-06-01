# !/usr/bin/python3
# -*- coding: utf-8 -*-

class SonicRespException(Exception):
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause
