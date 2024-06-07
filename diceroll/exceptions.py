class DicerollException(Exception):
    pass


class UsageError(DicerollException):
    pass


class InvalidArguments(DicerollException):
    """Invalid argument(s)"""


class NotRedisCommand(DicerollException):
    """Not a Redis command"""


class AmbiguousCommand(DicerollException):
    """Command is not finished, don't it's command's name"""


class NotSupport(DicerollException):
    """Diceroll currently not support this."""
