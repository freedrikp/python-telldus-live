import json

import requests
from requests_oauthlib import OAuth1

from .exceptions import TelldusRequestException
from .mixins import INSTALLED_MIXINS

class TelldusSession():
    device_ids = None
    sensor_ids = None

    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        oauth = OAuth1(
            config.get_public_key(),
            client_secret=config.get_private_key(),
            resource_owner_key=config.get_token(),
            resource_owner_secret=config.get_token_secret()
        )

        self.__session = requests.Session()
        self.__session.auth = oauth

        for name, mixin in INSTALLED_MIXINS.items():
            setattr(self, name, mixin(self))

    def communicate(self, url, params=None):
        full_url = 'https://api.telldus.com/json/%s' % url
        # if kwargs.get('local'):
        #     full_url = 'http://192.168.1.98/api/%s' % url
        # if 'local' in kwargs:
        #     del kwargs['local']
        response = self.__session.get(full_url, params=params)
        if response.status_code == requests.codes.ok:
            return response.json()
        raise TelldusRequestException(response)

    @staticmethod
    def pprint(json_data):
        print(json.dumps(json_data, indent=2, sort_keys=True))
