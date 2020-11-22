from ruption import *
from functools import partialmethod, partial
from array import array
from abc import ABC, abstractmethod
from types import FunctionType

__version__ = '0.1'


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
        elif isinstance(_, str):
            return self.as_str() == _
        raise False

    def __ne__(self, _):
        if isinstance(_, self.__class__):
            return self.has != _.has
        elif isinstance(_, str):
            return self.as_str() != _
        return True

    @classmethod
    def from_str(cls, string: str):
        new = cls()
        new.push_str(string)
        return new

    @classmethod
    def from_iterable(cls, iterable):
        new = cls()
        for i in iterable:
            new.push(i)
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

    def __repr__(self):
        return f'String("{self}")'

    __len__ = len = lambda self: self.has.__len__()
    length = property(len)

    def as_bytes(self, encoding):
        return list(bytearray(str(self), encoding))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.has.__getitem__(key)
        elif isinstance(key, int):
            return self.has[key]
        else:
            raise TypeError

    def __setitem__(self, key, value):
        self.has[key] = value

    def __delitem__(self, key):
        del self.has[key]

    def truncate(self, new_len):
        self.has = self[:new_len]

    def pop(self):
        try:
            return some(self.has.pop())
        except IndexError:
            return none

    def remove(self, idx):
        try:
            _ = self[idx]
            del self[idx]
            return some(_)
        except IndexError:
            return none

    def retain(self, f):
        self.has = self.init_store((_ for _ in self.has if f(_)))

    def check_bounds(self, idx):
        if not (0 <= idx <= len(self)):
            raise IndexError

    def check_range_bounds(self, rng):
        for _ in rng:
            self.check_bounds(_)

    def insert(self, idx, c):
        self.check_bounds(idx)
        self.has.insert(idx, c)

    def insert_str(self, idx, string):
        for i, s in enumerate(string):
            self.insert(idx + i, s)

    def __bool__(self):
        return len(self) != 0

    def is_empty(self):
        return len(self) == 0

    def split_off(self, at):
        self.check_bounds(at)

        _ = self.from_iterable(self[at:])
        self.truncate(at)
        return _

    def clear(self):
        self.has = self.init_store()

    def drain(self, rng):
        self.check_range_bounds(rng)

        _ = self.init_store()

        for i, r in enumerate(rng):
            _.append(self.remove(r-i).unwrap())

        return self.from_iterable(_)

    def replace_range(self, rng, replace_with):
        self.check_range_bounds(rng)

        if rng.step != 1:
            raise TypeError(f"Step in range {rng} must be 1. Period.")

        self.drain(rng)
        self.insert_str(rng[0], replace_with)
