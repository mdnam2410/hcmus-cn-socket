class SendingError(Exception):
    pass

class ReceivingError(Exception):
    pass

class ServerError(Exception):
    def __init__(self, message):
        super().__init__(message)

