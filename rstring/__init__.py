from functools import partialmethod, partial
from array import array

from ruption import *
from take import take



class String:
    'Mutable, change-friendly, feature-rich String.'

    init_store = partial(array, 'u')

    def __new__(cls, _=None, encoding=None):
        if _ is None:
            return super().__new__(cls)
        instance_of = partial(isinstance, _)

        if instance_of(str):
            return cls.from_str(_)
        elif instance_of(array) and _.typecode == 'u':
            return cls.from_unicode_array(_)
        elif instance_of(bytes):
            return cls.from_encoding(_, encoding)
        
        try:
            iter(_)
        except TypeError: ...
        else:
            return cls.from_iterable(_)

        raise TypeError(f'{cls.__qualname__} cannot be created from {_.__class__}')

    str_attrs = set(_ for _ in dir(str) if not _.startswith('__'))

    def __getattr__(self, name):
        if name == 'has':
            self.has = has = self.init_store()
            return has
        elif name in self.str_attrs:
            return lambda *args, **kwargs: getattr(str, name)(str(self), *args, **kwargs)

        raise AttributeError(name)

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
        new.extend(iterable)
        return new

    def extend(self, iterable):
        self.has.extend(iterable)

    @classmethod
    def from_unicode_array(cls, uar):
        new = cls()
        new[:] = uar
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
        return self.has.__getitem__(key)

    def __setitem__(self, key, value):
        self.has.__setitem__(key, value)

    def __delitem__(self, key):
        self.has.__delitem__(key)

    def truncate(self, new_len):
        self[:] = self[:new_len]

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
        self.set_store_from_iterable((_ for _ in self.has if f(_)))

    filter = retain

    def map(self, f):
        self.set_store_from_iterable(map(f, self[:]))
        return self

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

        _ = self.from_unicode_array(self[at:])
        self.truncate(at)
        return _

    def clear(self):
        self[:] = self.init_store()

    def drain(self, rng):
        self.check_range_bounds(rng)

        _ = self.init_store()

        for i, r in enumerate(rng):
            _.append(self.remove(r-i).unwrap())

        return self.from_unicode_array(_)

    def replace_range(self, rng, replace_with):
        self.check_range_bounds(rng)

        if rng.step != 1:
            raise TypeError(f"Step in {rng} must be 1. Period.")

        self.drain(rng)
        self.insert_str(rng[0], replace_with)

    def set_store_from_iterable(self, iterable):
        self[:] = self.init_store(iterable)

    def chars(self):
        return iter(self)

    def char_indices(self):
        return enumerate(self)

    def copy(self):
        new = self.new()
        new[:] = self[:]
        return new

    def __add__(self, _):
        if isinstance(_, self.__class__):
            return take(self.copy()).extend(_.has).unwrap()
        elif isinstance(_, str):
            return take(self.copy()).push_str(_).unwrap()
        else:
            raise NotImplementedError(_)

    def __radd__(self, _):
        if isinstance(_, str):
            return take(self.copy()).insert_str(0, _).unwrap()
        else:
            raise NotImplementedError(_)

    def strip_prefix(self, prefix, recurr=False):
        if len(prefix) > len(self):
            return

        for i, c in enumerate(prefix):
            if self[i] != c:
                break
        else:
            self[:] = self[len(prefix):]
            if recurr:
                self.strip_prefix(prefix, True)

    removeprefix = strip_prefix

    def strip_suffix(self, suffix, recurr=False):
        if len(suffix) > len(self):
            return

        for c1, c2 in zip(self[-len(suffix):], suffix):
            if c1 != c2:
                break
        else:
            self[:] = self[:len(self) - len(suffix)]
            if recurr:
                self.strip_suffix(suffix, True)


    removesuffix = strip_suffix