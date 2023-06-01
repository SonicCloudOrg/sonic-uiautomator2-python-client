# !/usr/bin/python3
# -*- coding: utf-8 -*-

# @Author: 花菜
# @File: sonic_exception.py
# @Time : 2023/6/1 17:35
# @Email: lihuacai168@gmail.com


class SonicRespException(Exception):
    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause
