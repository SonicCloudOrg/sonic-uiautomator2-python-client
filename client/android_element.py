# !/usr/bin/python3
# -*- coding: utf-8 -*-

import base64
import json
from abc import abstractmethod

from common.http_client import HttpUtil
from common.sonic_exception import SonicRespException
from common.models import ElementRect


class AndroidElement:
    def __init__(self, id: str, uia_client):
        self.id = id
        self.uia_client = uia_client
        self.logger = uia_client.get_logger()

    def click(self):
        self.uia_client.check_session_id()
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_post(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/click"
            )
        )
        if b.err is None:
            self.logger.info(f"click element {self.id}.")
        else:
            self.logger.error(f"click element {self.id} failed.")
            raise SonicRespException(b.err.message)

    def send_keys(self, text: str, is_cover: bool = False):
        self.uia_client.check_session_id()
        data = json.dumps({"text": text, "replace": is_cover})
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_post(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/value"
            ).body(data),
            60000,
        )
        if b.err is None:
            self.logger.info(f"send key to {self.id}.")
        else:
            self.logger.error(f"send key to {self.id} failed.")
            raise SonicRespException(b.err.message)

    def clear(self):
        self.uia_client.check_session_id()
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_post(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/clear"
            ),
            60000,
        )
        if b.err is None:
            self.logger.info(f"clear {self.id}.")
        else:
            self.logger.error(f"clear {self.id} failed.")
            raise SonicRespException(b.err.message)

    def get_text(self) -> str:
        self.uia_client.check_session_id()
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_get(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/text"
            )
        )
        if b.err is None:
            self.logger.info(f"get {self.id} text {b.value}.")
            return b.value
        else:
            self.logger.error(f"get {self.id} text failed.")
            raise SonicRespException(b.err.message)

    def get_attribute(self, name: str) -> str:
        self.uia_client.check_session_id()
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_get(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/attribute/{name}"
            )
        )
        if b.err is None:
            self.logger.info(f"get {self.id} attribute {name} result {b.value}.")
            return b.value
        else:
            self.logger.error(f"get {self.id} attribute failed.")
            raise SonicRespException(b.err.message)

    def get_uniquely_identifies(self) -> str:
        return self.id

    def get_rect(self) -> ElementRect:
        self.uia_client.check_session_id()
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_get(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/rect"
            )
        )
        if b.err is None:
            element_rect = ElementRect(**json.loads(b.value))
            self.logger.info(f"get {self.id} rect {element_rect}.")
            return element_rect
        else:
            self.logger.error(f"get {self.id} rect failed.")
            raise SonicRespException(b.err.message)

    def screenshot(self) -> bytes:
        self.uia_client.check_session_id()
        b = self.uia_client.get_resp_handler().get_resp(
            HttpUtil.create_get(
                f"{self.uia_client.remote_url}/session/{self.uia_client.get_session_id()}/element/{self.id}/screenshot"
            ),
            60000,
        )
        if b.err is None:
            self.logger.info(f"get element {self.id} screenshot.")
            return base64.b64decode(b.value)
        else:
            self.logger.error(f"get element {self.id} screenshot failed.")
            raise SonicRespException(b.err.message)
