class pwnmapCommandException(Exception):
    pass


class UsageException(pwnmapCommandException):
    pass


class ArgumentValueError(pwnmapCommandException):
    pass
