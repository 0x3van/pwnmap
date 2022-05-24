class _Optional:
    __slots__ = ('_name', '__doc__', '_getitem')

    def __init__(self, getitem):
        self._getitem = getitem
        self._name = getitem.__name__
        self.__doc__ = getitem.__doc__

    def __reduce__(self):
        return self._name

    def __getitem__(self, key):
        return self._getitem(self, key)


@_Optional
def Optional(self, _type):
    if not _type:
        raise TypeError('Cannot take an Optional command argument of no types.')
    return self, _type
