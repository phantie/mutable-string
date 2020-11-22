from ruption import *
from functools import partialmethod, partial
from array import array
from abc import ABC, abstractmethod
from types import FunctionType

__version__ = '0.1'


class Node:
    pass

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
        new.has = cls.init_store(iter(string))
        return new

    @classmethod
    def from_encoding(cls, bytes, encoding):
        return cls.from_str(bytes.decode(encoding))

    from_utf8 = partialmethod(from_encoding, encoding='utf-8')

    def push(self, c):
        self.has.append(c)

    def push_str(self, string):
        self.has.extend(iter(string))

    __str__ = to_str = as_str = lambda self: "".join(self.has)

    def __len__(self):
        return self.has.__len__()

    def len(self):
        return self.has.__len__()
