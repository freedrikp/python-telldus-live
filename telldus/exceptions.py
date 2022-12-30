

class TelldusRequestException(Exception):
    # TODO: Extend this to print relevant response data in message
    pass

class TelldusRequestClientError(TelldusRequestException):
    pass

class TelldusRequestServerError(TelldusRequestException):
    pass
