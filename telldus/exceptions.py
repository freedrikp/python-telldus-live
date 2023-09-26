

class TelldusRequestException(Exception):
    # TODO: Extend this to print relevant response data in message

    @property
    def status_code(self):
        response, = self.args
        return response.status_code

class TelldusRequestClientError(TelldusRequestException):
    pass

class TelldusRequestServerError(TelldusRequestException):
    pass

class TelldusRequestPayloadError(TelldusRequestException):
    pass
