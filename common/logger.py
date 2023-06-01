# !/usr/bin/python3
# -*- coding: utf-8 -*-

import logging


class Logger:
    def __init__(self):
        self.formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.isShowLog = True
        self.logger = logging.getLogger("sonic-driver-core")
        self.set_log_level(logging.INFO)

        ch = logging.StreamHandler()
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

    def set_log_level(self, level):
        self.logger.setLevel(level)

    def show_log(self):
        self.isShowLog = True
        self.set_log_level(logging.INFO)

    def disable_log(self):
        self.isShowLog = False
        self.set_log_level(logging.CRITICAL)

    def info(self, msg, *args):
        if self.isShowLog:
            self.logger.info(msg, *args)

    def error(self, msg, *args):
        if self.isShowLog:
            self.logger.error(msg, *args)
