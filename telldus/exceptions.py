

class TelldusRequestException(Exception):

    def __init__(self, response):
        self.__response = response
        message = '%s\n%s\n%s' % (response.status_code, response.headers, response.text)
        super().__init__(message)

    @property
    def status_code(self):
        return self.__response.status_code

class TelldusRequestClientError(TelldusRequestException):
    pass

class TelldusRequestServerError(TelldusRequestException):
    pass

class TelldusRequestPayloadError(TelldusRequestException):
    pass
