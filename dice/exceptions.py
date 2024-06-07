class diceException(Exception):
    pass


class UsageError(diceException):
    pass


class InvalidArguments(diceException):
    """Invalid argument(s)"""


class NotRedisCommand(diceException):
    """Not a Redis command"""


class AmbiguousCommand(diceException):
    """Command is not finished, don't it's command's name"""


class NotSupport(diceException):
    """dice currently not support this."""
