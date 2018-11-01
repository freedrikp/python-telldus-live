import json

import requests
from requests_oauthlib import OAuth1Session, OAuth1

from exceptions import TelldusRequestException

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

    def communicate(self, url, params=None):
        full_url = 'https://api.telldus.com/json/%s' % url
        # if kwargs.get('local'):
        #     full_url = 'http://192.168.1.98/api/%s' % url
        # if 'local' in kwargs:
        #     del kwargs['local']
        response = self.__session.get(full_url, params=params)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print(response.text)
            raise TelldusRequestException(response)

    @staticmethod
    def pprint(json_data):
        print(json.dumps(json_data, indent=2, sort_keys=True))

    def get_device_id(self, device_name):
        if not self.device_ids:
            self.device_ids = {}
            devices = self.communicate('devices/list')
            for device in devices['device']:
                self.device_ids[device['name']] = device['id']

        return self.device_ids[device_name]

    def __device_action(self, action, device):
        device_id = device if device.isdigit() else self.get_device_id(device)
        return self.communicate('device/%s' % action, params={'id':device_id})

    def turn_on_device(self, device):
        return self.__device_action('turnOn', device)

    def turn_off_device(self, device):
        return self.__device_action('turnOff', device)

    def get_sensor_id(self, sensor_name):
        if not self.sensor_ids:
            self.sensor_ids = {}
            sensors = self.communicate('sensors/list')
            for sensor in sensors['sensor']:
                self.sensor_ids[sensor['name']] = sensor['id']

        return self.sensor_ids[sensor_name]

    def __sensor_action(self, action, sensor):
        sensor_id = sensor if sensor.isdigit() else self.get_sensor_id(sensor)
        return self.communicate('sensor/%s' % action, params={'id':sensor_id})

    def sensor_info(self, sensor):
        return self.__sensor_action('info', sensor)
