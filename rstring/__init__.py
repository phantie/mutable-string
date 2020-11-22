from ruption import *
from functools import partialmethod, partial
from array import array
from abc import ABC, abstractmethod
from types import FunctionType

__version__ = '0.1'

# class Char:
#     def __new__(cls, char):
#         assert isinstance(char, str)
#         assert char.__len__() == 1
#         return char

class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)

class staticproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f()

# class SomeMetaclass(type):
#     def __new__(cls, name, bases, attrs):
#         if isinstance(attrs['init_store'], FunctionType):
#             attrs['init_store'] = attrs['init_store']()
#         return super().__new__(cls, name, bases, attrs)

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

    def __str__(self):
        return "".join(self.has)

    def __len__(self):
        return self.has.__len__()

    def len(self):
        return self.has.__len__()

from timeit import timeit
from string import ascii_letters
from random import shuffle

def split_every(n, l):
    result = []
    step = n
    while True:
        result.append(l[n - step: n])
        n+=step

        if n > len(l):
            if (left := l[n - step:]):
                result.append(left)
            break

    return result

long_str = list(ascii_letters * 100) 
shuffle(long_str)
long_str = ''.join(long_str)

split_long_str = partial(split_every, l = long_str)

kit = dict (
    e1 = list(long_str),
    e2 = split_long_str(2),
    e5 = split_long_str(5),
    e20 = split_long_str(20),
    e50 = split_long_str(50),
    e150 = split_long_str(150),
    e500 = split_long_str(500),
    e1500 = split_long_str(1500),
    e3500 = split_long_str(3500),
)

for k, v in kit.items():
    print(k, timeit(lambda: ''.join(v), number=10000))
