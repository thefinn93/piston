from piston.exceptions import PistonException


class InvalidTokenException(PistonException):
    status_code = 401


class UnknownEndpointException(PistonException):
    pass
