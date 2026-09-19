import abc
import json

class BaseTelldusConfiguration(abc.ABC):

    @abc.abstractmethod
    def get_public_key(self):
        return None

    @abc.abstractmethod
    def get_private_key(self):
        return None

    @abc.abstractmethod
    def get_token(self):
        return None

    @abc.abstractmethod
    def get_token_secret(self):
        return None

    @abc.abstractmethod
    def get_access_token(self):
        return None

    @abc.abstractmethod
    def get_local_address(self):
        return None

    @abc.abstractmethod
    def get_local_client_name(self):
        return None

class JSONTelldusConfiguraton(BaseTelldusConfiguration):

    def __init__(self, json_file):
        with open(json_file) as file_obj:
            self.json_data = json.load(file_obj)

    def get_public_key(self):
        return self.json_data['public_key']

    def get_private_key(self):
        return self.json_data['private_key']

    def get_token(self):
        return self.json_data['token']

    def get_token_secret(self):
        return self.json_data['token_secret']

    def get_access_token(self):
        return self.json_data['access_token']

    def get_local_address(self):
        return self.json_data['local_address']

    def get_local_client_name(self):
        return self.json_data['local_client_name']

# TODO create a Oauth 1.0 workflow Configuration class
