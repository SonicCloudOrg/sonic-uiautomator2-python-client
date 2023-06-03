from client.uia_client import UiaClient


# Android Driver with uia client.
class AndroidDriver(object):

    def __init__(self, url):
        self._client = UiaClient()
        self._client.remote_url = url
        self._client.new_session({})

