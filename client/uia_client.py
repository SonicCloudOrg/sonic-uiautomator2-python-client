import json
import time
from base64 import b64decode, b64encode
from typing import Any, Dict, List


from client.android_element import AndroidElement, AndroidElementImpl
from common.http_client import HttpUtil
from common.logger import Logger
from common.resp_handler import RespHandler
from exceptions.sonic_resp_exception import SonicRespException
from models import BaseResp, ErrorMsg, Method, SessionInfo, WindowSize

DEFAULT_REQUEST_TIMEOUT = 15000

# Client of uiautomator2 server, see https://github.com/appium/appium-uiautomator2-server


# class UiaClient(object):
#     def __init__(self):
#         self._session_id = ""
#         self._url = ""
#         self._req = requests
#         self._req.Timeout = DEFAULT_REQUEST_TIMEOUT
#
#     def set_remote_url(self, url):
#         self._url = url
#
#     def new_session(self, capabilities=None):
#         if capabilities is None:
#             capabilities = {}
#
#         data = {"capabilities": capabilities}
#
#         try:
#             res = self._req.post(self._url + "/session", data)
#             self._session_id = res.sessionId
#         except SonicRespException:
#             raise


class UiaClientImpl:
    LEGACY_WEB_ELEMENT_IDENTIFIER = "ELEMENT"
    WEB_ELEMENT_IDENTIFIER = "element-6066-11e4-a52e-4f735466cecf"
    FIND_ELEMENT_INTERVAL = 3000
    FIND_ELEMENT_RETRY = 5

    def __init__(self):
        self.remote_url = ""
        self.session_id = ""
        self.resp_handler = RespHandler()
        self.logger = Logger()
        self.size = None

    def check_bundle_id(self, bundleId: str):
        if not bundleId:
            self.logger.error("bundleId not found.")
            raise SonicRespException("bundleId not found.")

    def parse_element_id(self, o: Any) -> str:
        jsonObject = json.loads(o)
        identifier = [self.LEGACY_WEB_ELEMENT_IDENTIFIER, self.WEB_ELEMENT_IDENTIFIER]
        for i in identifier:
            result = jsonObject.get(i, "")
            if result:
                return result
        return ""

    def new_session(self, capabilities: Dict):
        data = {"capabilities": capabilities}
        b: BaseResp = self.resp_handler.get_resp(
            HttpUtil.create_post(self.remote_url + "/session").body(json.dumps(data))
        )
        if b.get_err() is None:
            # TODO parse session id
            sessionInfo = SessionInfo.parse(b)
            self.session_id = sessionInfo.get_session_id()
            self.logger.info("start session successful!")
            self.logger.info("session : %s", self.session_id)
        else:
            self.logger.error("start session failed.")
            self.logger.error("cause: %s", b.get_err().get_message())
            raise SonicRespException(b.get_err().get_message())

    def close_session(self):
        self.check_session_id()
        self.resp_handler.get_resp(
            HttpUtil.create_request(
                Method.DELETE, self.remote_url + "/session/" + self.session_id
            )
        )
        self.logger.info("close session successful!")

    def check_session_id(self):
        if not self.session_id:
            self.logger.error("sessionId not found.")
            raise SonicRespException("sessionId not found.")

    def get_window_size(self):
        if self.size is None:
            self.check_session_id()
            b: BaseResp = self.resp_handler.get_resp(
                HttpUtil.create_get(
                    self.remote_url
                    + "/session/"
                    + self.session_id
                    + "/window/:windowHandle/size"
                )
            )
            if b.get_err() is None:
                # TODO parse window size
                self.size = WindowSize.parse(b)
                self.logger.info("get window size %s.", self.size.to_string())
            else:
                self.logger.error("get window size failed.")
                raise SonicRespException(b.get_err().get_message())
        return self.size

    def send_keys(self, text: str, is_cover: bool):
        self.check_session_id()
        data = {"text": text, "replace": is_cover}
        b = self.resp_handler.get_resp(
            HttpUtil.create_post(
                self.remote_url + "/session/" + self.session_id + "/keys"
            ).body(json.dumps(data))
        )
        if b.get_err() is None:
            self.logger.info("send key %s.", text)
        else:
            self.logger.error("send key failed.")
            raise SonicRespException(b.get_err().get_message())

    def set_pasteboard(self, content_type: str, content: str):
        self.check_session_id()
        data = {
            "contentType": content_type.upper(),
            "content": b64encode(content.encode()).decode(),
        }
        b = self.resp_handler.get_resp(
            HttpUtil.create_post(
                self.remote_url
                + "/session/"
                + self.session_id
                + "/appium/device/set_clipboard"
            ).body(json.dumps(data))
        )
        if b.get_err() is None:
            self.logger.info("set pasteboard %s.", content)
        else:
            self.logger.error("set pasteboard failed.")
            raise SonicRespException(b.get_err().get_message())

    def get_pasteboard(self, content_type: str) -> bytes:
        self.check_session_id()
        data = {"contentType": content_type.upper()}
        b = self.resp_handler.get_resp(
            HttpUtil.create_post(
                self.remote_url
                + "/session/"
                + self.session_id
                + "/appium/device/get_clipboard"
            ).body(json.dumps(data))
        )
        if b.get_err() is None:
            result = b64decode(b.get_value())
            self.logger.info("get pasteboard length: %d.", len(result))
            return result
        else:
            self.logger.error("get pasteboard failed.")
            raise SonicRespException(b.get_err().get_message())

    def page_source(self) -> str:
        self.check_session_id()
        b = self.resp_handler.get_resp(
            HttpUtil.create_get(
                self.remote_url + "/session/" + self.session_id + "/source"
            ),
            60000,
        )
        if b.get_err() is None:
            self.logger.info("get page source.")
            return b.get_value()
        else:
            self.logger.error("get page source failed.")
            raise SonicRespException(b.get_err().get_message())

    def set_default_find_element_interval(
        self, retry: int = None, interval: int = None
    ):
        if retry is not None:
            self.FIND_ELEMENT_RETRY = retry
        if interval is not None:
            self.FIND_ELEMENT_INTERVAL = interval

    def find_element(
        self, selector: str, value: str, retry: int = None, interval: int = None
    ) -> AndroidElement:
        androidElement = None
        wait = 0
        intervalInit = self.FIND_ELEMENT_INTERVAL if interval is None else interval
        retryInit = self.FIND_ELEMENT_RETRY if retry is None else retry
        errMsg = ""
        while wait < retryInit:
            wait += 1
            self.check_session_id()
            data = {"strategy": selector, "selector": value}
            b = self.resp_handler.get_resp(
                HttpUtil.create_post(
                    self.remote_url + "/session/" + self.session_id + "/element"
                ).body(json.dumps(data))
            )
            if b.get_err() is None:
                self.logger.info("find element successful.")
                id = self.parse_element_id(b.get_value())
                if len(id) > 0:
                    androidElement = AndroidElementImpl(id, self)
                    break
                else:
                    self.logger.error(
                        "parse element id %s failed. retried %d times, retry in %d ms.",
                        b.get_value(),
                        wait,
                        intervalInit,
                    )
            else:
                self.logger.error(
                    "element not found. retried %d times, retry in %d ms.",
                    wait,
                    intervalInit,
                )
                errMsg = b.get_err().get_message()
            if wait < retryInit:
                time.sleep(intervalInit / 1000)
        if androidElement is None:
            raise SonicRespException(errMsg)
        return androidElement

    def find_element_list(
        self, selector: str, value: str, retry: int = None, interval: int = None
    ) -> List[AndroidElement]:
        androidElementList = []
        wait = 0
        intervalInit = self.FIND_ELEMENT_INTERVAL if interval is None else interval
        retryInit = self.FIND_ELEMENT_RETRY if retry is None else retry
        errMsg = ""
        while wait < retryInit:
            wait += 1
            self.check_session_id()
            data = {"strategy": selector, "selector": value}
            b = self.resp_handler.get_resp(
                HttpUtil.create_post(
                    self.remote_url + "/session/" + self.session_id + "/elements"
                ).body(json.dumps(data))
            )
            if b.get_err() is None:
                self.logger.info("find elements successful.")
                ids = json.loads(b.get_value())
                for ele in ids:
                    id = self.parse_element_id(ele)
                    if len(id) > 0:
                        androidElementList.append(AndroidElementImpl(id, self))
                    else:
                        self.logger.error("parse element id %s failed.", ele)
                        continue
                break
            else:
                self.logger.error(
                    "elements not found. retried %d times, retry in %d ms.",
                    wait,
                    intervalInit,
                )
                errMsg = b.get_err().get_message()
            if wait < retryInit:
                time.sleep(intervalInit / 1000)
        if len(androidElementList) == 0:
            raise SonicRespException(errMsg)
        return androidElementList

    def screenshot(self) -> bytes:
        self.check_session_id()
        b = self.resp_handler.get_resp(
            HttpUtil.create_get(
                self.remote_url + "/session/" + self.session_id + "/screenshot"
            ),
            60000,
        )
        if b.get_err() is None:
            self.logger.info("get screenshot.")
            return b64decode(b.get_value())
        else:
            self.logger.error("get screenshot failed.")
            raise SonicRespException(b.get_err().get_message())

    def set_appium_settings(self, settings: dict):
        self.check_session_id()
        data = {"settings": settings}
        b = self.resp_handler.get_resp(
            HttpUtil.create_post(
                self.remote_url + "/session/" + self.session_id + "/appium/settings"
            ).body(json.dumps(data))
        )
        if b.get_err() is None:
            self.logger.info("set appium settings %s.", json.dumps(settings))
        else:
            self.logger.error("set appium settings failed.")
            raise SonicRespException(b.get_err().get_message())
