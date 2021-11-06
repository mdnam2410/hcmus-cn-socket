class SendingError(Exception):
    pass

class ReceivingError(Exception):
    pass

class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ClientError(Exception):
    def __init__(self, message) -> None:
        super().__init__(message)