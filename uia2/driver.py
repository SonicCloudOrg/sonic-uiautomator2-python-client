from client.uia_client import UiaClient
from common.resp_handler import RespHandler


# Android Driver with uia client.
class AndroidDriver(object):

    def __init__(self, url, cap=None, timeout=RespHandler.DEFAULT_REQUEST_TIMEOUT):
        if cap is None:
            cap = {}
        self._client = UiaClient()
        self._client.remote_url = url
        self._client.resp_handler.set_request_timeout(timeout)
        self._client.new_session(cap)

    def get_page_source(self):
        return self._client.page_source()
