"""Exception for PythonMailer"""

class MessageExeption(Exception):
    """Base class for all exceptions raised by this module."""


class InvalidAddressHeader(MessageExeption):
    """Use no valid address header"""

    def __init__(self, message):
        self.message = message


class InvalidAddress(MessageExeption):
    """Use no valid email address"""

    def __init__(self, message):
        self.message = message


class EmptyBody(MessageExeption):
    """Message body not set"""

    def __init__(self, message):
        self.message = message


class EmptyAddr(MessageExeption):
    """Required email address is empty"""

    def __init__(self, message):
        self.message = message


class SenderExeption(Exception):
    """Base class for all exceptions raised by this module."""


class EmptyRecipients(SenderExeption):
    """Try send message which no have recipients."""


class SendingError(SenderExeption):
    """Error when sending message."""

    def __init__(self, message):
        self.message = message
