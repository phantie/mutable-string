from ruption import *
from functools import partialmethod, partial
from array import array
from abc import ABC, abstractmethod
from types import FunctionType

__version__ = '0.1'

s = 32

def split_every(l, n):
    return list(l[i:i+n] for i in range(0, len(l), n))

class String:

    init_store = partial(array, 'u')

    def __init__(self):
        self.has = self.init_store()

    @classmethod
    def new(cls):
        return cls()

    def __eq__(self, _):
        if isinstance(_, self.__class__):
            return self.has == _.has
        raise False

    def __ne__(self, _):
        if isinstance(_, self.__class__):
            return self.has != _.has
        return True

    @classmethod
    def from_str(cls, string: str):
        new = cls()
        new.push_str(string)
        return new

    @classmethod
    def from_encoding(cls, bytes, encoding):
        return cls.from_str(bytes.decode(encoding))

    from_utf8 = partialmethod(from_encoding, encoding='utf-8')

    def push(self, c):
        self.has.append(c)

    def push_str(self, string):
        self.has.fromunicode(string)

    def __str__(self):
        return self.has.tounicode()

    to_str = as_str = __str__

    __len__ = len = lambda self: self.has.__len__()
    length = property(len)