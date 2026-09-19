import json

import requests
from requests_oauthlib import OAuth1
from requests.auth import AuthBase

from .exceptions import *
from .mixins import INSTALLED_MIXINS


class TokenAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers['Authorization'] = "Bearer %s" % self.token
        return request

class TelldusSession():
    device_ids = None
    sensor_ids = None

    def __init__(self, address, auth):

        self._session = requests.Session()
        self._session.auth = auth
        self.__address = address

        for name, mixin in INSTALLED_MIXINS.items():
            setattr(self, name, mixin(self))

    def communicate(self, url, params=None):
        full_url = '%s/%s' % (self.__address, url)
        response = self._session.get(full_url, params=params)
        if response.ok:
            try:
                return response.json()
            except:
                raise TelldusRequestPayloadError(response)
        if response.status_code >= 500:
            raise TelldusRequestServerError(response)
        if response.status_code >= 400:
            raise TelldusRequestClientError(response)
        raise TelldusRequestException(response)

    @staticmethod
    def pprint(json_data):
        print(json.dumps(json_data, indent=2, sort_keys=True))

class TelldusLiveSession(TelldusSession):

    def __init__(self, config):
        oauth = OAuth1(
            config.get_public_key(),
            client_secret=config.get_private_key(),
            resource_owner_key=config.get_token(),
            resource_owner_secret=config.get_token_secret()
        )
        super().__init__("https://pa-api.telldus.com/json", oauth)

class TelldusLocalSession(TelldusSession):

    def __init__(self, config):
        token_auth = TokenAuth(config.get_access_token())
        address = "%s/api" % config.get_local_address()
        super().__init__(address, token_auth)
        self.__client_name = config.get_local_client_name()

    def communicate(self, url, params=None):
        response = super().communicate(url, params=params)
        if url.rpartition("/")[2] == "list":
            for value in response.values():
                for item in value:
                    if "clientName" not in item:
                        item["clientName"] = self.__client_name
        return response
