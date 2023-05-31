import requests

from exceptions.sonic_resp_exception import SonicRespException

DEFAULT_REQUEST_TIMEOUT = 15000


# Client of uiautomator2 server, see https://github.com/appium/appium-uiautomator2-server
class UiaClient(object):

    def __init__(self):
        self._session_id = ""
        self._url = ""
        self._req = requests
        self._req.Timeout = DEFAULT_REQUEST_TIMEOUT

    def set_remote_url(self, url):
        self._url = url

    def new_session(self, capabilities=None):
        if capabilities is None:
            capabilities = {}

        data = {
            "capabilities": capabilities
        }

        try:
            res = self._req.post(self._url + '/session', data)
            self._session_id = res.sessionId
        except SonicRespException:
            raise
