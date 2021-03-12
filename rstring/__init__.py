from __future__ import annotations
from functools import partialmethod, wraps
from array import array
from typing import NewType, Union, Callable, Iterable, Generator, Type

from ruption import some, none
from take import take

__all__ = ('String',)
__version__ = '0.5.2'


def no_mut(f):
    if __debug__:
        @wraps(f)
        def wrap(self, *args, **kwargs):
            before = self.new()
            before[:] = self[:]

            after = self

            result = f(self, *args, **kwargs)
            assert after[:] == before[:]
            return result
        return wrap
    else:
        return f


class String(array):
    'Mutable, change-friendly, feature-rich String.'

    @staticmethod
    def __new__(cls, o=None, encoding=None) -> Self:

        if not o:
            return super().__new__(cls, 'u')

        o_cls_inh = set(o.__class__.__mro__)

        if str in o_cls_inh:
            return cls.from_str(o)
        elif array in o_cls_inh:
            return cls.from_unicode_array(o)
        elif bytes in o_cls_inh:
            return cls.from_encoding(o, encoding)

        try:
            iterable = iter(o)
        except TypeError:
            raise TypeError(f'{cls.__qualname__} cannot be created from {o.__class__}')
        else:
            return cls.from_iterable(iterable)

    _str_attrs = set(_ for _ in dir(str) if not _.startswith('__')).union(set(('removeprefix', 'removesuffix')))

    def __getattr__(self, name):
        if name in self._str_attrs:
            return lambda *args, **kwargs: getattr(str, name)(str(self), *args, **kwargs)

        raise AttributeError(name)

    @classmethod
    def new(cls) -> Self:
        return super().__new__(cls, 'u')

    @no_mut
    def __eq__(self, _) -> bool:
        if isinstance(_, self.__class__):
            return super().__eq__(_)
        elif isinstance(_, str):
            return self.as_str() == _
        return False

    @no_mut
    def __ne__(self, _) -> bool:
        if isinstance(_, self.__class__):
            return super().__ne__(_)
        elif isinstance(_, str):
            return self.as_str() != _
        return True

    @no_mut
    def __ge__(self, _):
        if isinstance(_, self.__class__):
            return super().__ge__(_)
        elif isinstance(_, str):
            return str(self) >= _
        else:
            raise TypeError("'>=' not supported between instances of 'String' and", repr(_.__class__.__name__))

    @no_mut
    def __le__(self, _):
        if isinstance(_, self.__class__):
            return super().__le__(_)
        elif isinstance(_, str):
            return str(self) <= _
        else:
            raise TypeError("'<=' not supported between instances of 'String' and", repr(_.__class__.__name__))

    @no_mut
    def __gt__(self, _):
        if isinstance(_, self.__class__):
            return super().__gt__(_)
        elif isinstance(_, str):
            return str(self) > _
        else:
            raise TypeError("'>' not supported between instances of 'String' and", repr(_.__class__.__name__))

    @no_mut
    def __lt__(self, _):
        if isinstance(_, self.__class__):
            return super().__lt__(_)
        elif isinstance(_, str):
            return str(self) < _
        else:
            raise TypeError("'<' not supported between instances of 'String' and", repr(_.__class__.__name__))

    @classmethod
    def from_str(cls, string: str) -> Self:
        new = super().__new__(cls, 'u')
        new.push_str(string)
        return new

    @classmethod
    def from_iterable(cls, iterable: Iterable) -> Self:
        new = super().__new__(cls, 'u')
        new.extend(iterable)
        return new

    @classmethod
    def from_unicode_array(cls, uar: array[u]) -> Self:
        new = super().__new__(cls, 'u')
        new[:] = uar
        return new

    @classmethod
    def from_encoding(cls, bytes: bytes, encoding: str) -> Self:
        return cls.from_str(bytes.decode(encoding))

    from_utf8 = partialmethod(from_encoding, encoding='utf-8')

    def push(self, _: u):
        self.append(_)

    def push_str(self, _: str):
        self.fromunicode(_)

    @no_mut
    def __str__(self) -> str:
        return self.tounicode()

    to_str = as_str = __str__

    @no_mut
    def __repr__(self) -> str:
        return f'String("{self}")'

    len = lambda self: self.__len__()
    length = property(len)

    @no_mut
    def as_bytes(self, encoding) -> [int]:
        return list(bytearray(str(self), encoding))

    def truncate(self, new_len: int):
        self[:] = self[:new_len]

    def pop(self) -> Option[u]:
        try:
            return some(super().pop())
        except IndexError:
            return none

    def remove(self, idx: int) -> Option[u]:
        try:
            _ = self[idx]
            del self[idx]
            return some(_)
        except IndexError:
            return none

    def retain(self, f: Callable[[u], bool]):
        self._set_store_from_iterable((_ for _ in self if f(_)))

    filter = retain

    def map(self, f: Callable[[u], u]):
        self._set_store_from_iterable(map(f, self[:]))

    def _check_bounds(self, idx: int):
        if not (0 <= idx <= len(self)):
            raise IndexError

    def _check_range_bounds(self, rng: range):
        for _ in rng:
            self._check_bounds(_)

    def insert(self, idx: int, u: u):
        self._check_bounds(idx)
        super().insert(idx, u)

    def insert_str(self, idx: int, string: str):
        for i, s in enumerate(string):
            self.insert(idx + i, s)

    @no_mut
    def is_empty(self) -> bool:
        return not bool(self)

    def split_off(self, at: int) -> Self:
        _ = self.take_from(at)
        self.truncate(at)
        return _

    def take_from(self, idx: int) -> Self:
        self._check_bounds(idx)
        return self.from_unicode_array(self[idx:])

    def clear(self):
        self[:] = self[:0]

    def drain(self, rng: range) -> Self:
        self._check_range_bounds(rng)

        _ = self.new()

        for i, r in enumerate(rng):
            _.push(self.remove(r-i).unwrap())

        return _

    def replace_range(self, rng: range, replace_with: str):
        self._check_range_bounds(rng)

        if rng.step != 1:
            raise TypeError(f"Step in {rng} must be 1. Period.")

        self.drain(rng)
        self.insert_str(rng[0], replace_with)

    def _set_store_from_iterable(self, iterable: Iterable):
        self[:] = self.from_iterable(iterable)

    @no_mut
    def chars(self) -> Iterable[u]:
        return iter(self)

    @no_mut
    def char_indices(self) -> Iterable[(int, u)]:
        return enumerate(self)

    @no_mut
    def copy(self) -> Self:
        new = self.new()
        new[:] = self[:]
        return new

    @no_mut
    def __add__(self, _) -> Self:
        if isinstance(_, self.__class__):
            return take(self.copy()).extend(_).unwrap()
        elif isinstance(_, str):
            return take(self.copy()).push_str(_).unwrap()
        else:
            raise NotImplementedError(_)

    @no_mut
    def __radd__(self, _) -> Self:
        if isinstance(_, str):
            return take(self.copy()).insert_str(0, _).unwrap()
        else:
            raise NotImplementedError(_)

    def strip_prefix(self, prefix: str, recurr: bool = False):
        if len(prefix) > len(self):
            return

        for this, opposite in zip(self, prefix):
            if this != opposite:
                break
        else:
            self[:] = self[len(prefix):]
            if recurr:
                self.strip_prefix(prefix, True)

    removeprefix = strip_prefix

    def strip_suffix(self, suffix: str, recurr: bool = False):
        if len(suffix) > len(self):
            return

        for this, opposite in zip(self[-len(suffix):], suffix):
            if this != opposite:
                break
        else:
            self[:] = self[:len(self) - len(suffix)]
            if recurr:
                self.strip_suffix(suffix, True)

    removesuffix = strip_suffix

    @no_mut
    def __mul__(self, other: int) -> Self:
        if isinstance(other, int):
            return self.from_unicode_array(self[:]*other)
        else:
            raise NotImplementedError

    repeat = __rmul__ = __mul__

    @classmethod
    def has_custom_impl(cls, methodname: str) -> bool:
        if methodname in cls._str_attrs:
            return methodname in dir(cls)
        else:
            raise AttributeError(f'{str} has no method named "{methodname}" ')

    @no_mut
    def split_at(self, mid: int) -> (Self, Self):
        first = self.from_unicode_array(self[:mid])
        last = self.from_unicode_array(self[mid:])
        return first, last

    @no_mut
    def lines(self) -> [str]:
        return self.splitlines()

    @no_mut
    def __contains__(self, _: Union[array[u], str, Self]) -> bool:
        if isinstance(_, str):
            return _ in str(self)
        elif isinstance(_, self.__class__):
            return str(_) in str(self)

        raise TypeError(f"'in <String>' requires str/String/array[u] as left operand, not {type(_).__qualname__}")

    contains = __contains__

    @no_mut
    def split_inclusive(self, sep: u) -> Generator[str]:
        assert len(sep) == 1
        def incapsulated_generator():
            prev = 0
            for i, _ in enumerate(self, 1):
                if _ == sep:
                    yield self[prev:i].tounicode()
                    prev = i
            if prev != len(self):
                yield self[prev:].tounicode()
        return incapsulated_generator()

    def collect(self, _: Type) -> Any:
        return _(self)

    @no_mut
    def char_index(self, u: u) -> Option[int]:
        try:
            return some(self.index(u))
        except ValueError:
            return none

    @no_mut
    def rchar_index(self, u: u) -> Option[int]:
        try:
            return some(len(self) - 1 - self[::-1].index(u))
        except ValueError:
            return none

    @no_mut
    def split_once(self, u: u) -> Option[(str, str)]:
        opt_idx = self.char_index(u)
        if opt_idx is none: return none
        first, last = self.split_at(opt_idx.unwrap())
        last.remove(0)
        return some((str(first), str(last)))

    @no_mut
    def rsplit_once(self, u: u) -> Option[(str, str)]:
        opt_idx = self.rchar_index(u)
        if opt_idx is none: return none
        first, last = self.split_at(opt_idx.unwrap())
        last.remove(0)
        return some((str(first), str(last)))

    def reverse(self):
        self[:] = self[::-1]

    def trim(self):
        self.trimr()
        self.triml()

    def trimr(self):
        self.removesuffix('\x20', recurr=True)

    def triml(self):
        self.removeprefix('\x20', recurr=True)

    def triml_num(self, num: int):
        assert num >= 0
        self[:] = self[num:]

    def trimr_num(self, num: int):
        assert num >= 0
        end = len(self)-num
        self[:] = self[:end if end > 0 else 0]

    def trim_num(self, num: int):
        assert num >= 0
        self.trimr_num(num)
        self.triml_num(num)

Self = String
u = NewType('u', str) # unicode character