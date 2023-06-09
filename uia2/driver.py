from client.uia_client import UiaClient
from common.models import PasteboardType, AndroidSelector
from common.resp_handler import RespHandler


# Android Driver with uia client.
class AndroidDriver(object):

    def __init__(self, url, cap=None, session_id=None, timeout=RespHandler.DEFAULT_REQUEST_TIMEOUT):
        if cap is None:
            cap = {}
        self._client = UiaClient()
        self._client.remote_url = url
        self._client.resp_handler.set_request_timeout(timeout)
        if session_id is None:
            self._client.new_session(cap)
        else:
            self._client.session_id = session_id

    def close_driver(self):
        self._client.close_session()

    def get_session_id(self):
        return self._client.session_id

    def get_uia_client(self):
        return self._client

    def get_window_size(self):
        return self._client.get_window_size()

    def send_keys(self, text: str, is_cover=None):
        if is_cover is None:
            is_cover = False
        self._client.send_keys(text, is_cover)

    def set_pasteboard(self, content_type: str, content: str):
        self._client.set_pasteboard(content_type, content)

    def get_pasteboard(self, content_type: str):
        return self._client.get_pasteboard(content_type)

    def get_page_source(self):
        return self._client.page_source()

    def set_default_find_element_interval(self, retry: int, interval: int):
        self._client.set_default_find_element_interval(retry, interval)

    def find_element(self, selector: AndroidSelector, value: str, retry: int = None, interval: int = None):
        return self._client.find_element(selector.value, value, retry, interval)

    def find_element_list(self, selector: AndroidSelector, value: str, retry: int = None, interval: int = None):
        return self._client.find_element_list(selector.value, value, retry, interval)

    def screenshot(self):
        return self._client.screenshot()

    def set_appium_settings(self, settings: dict):
        self._client.set_appium_settings(settings)
