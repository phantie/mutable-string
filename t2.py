from array import array

a = array('u', '12345')


class MutableSlice:

    def __init__(self, to, start = 0, stop = None):
        self.to = to
        self.start = start
        self.stop = stop

    def __repr__(self):
        return f'MutableSlice[{self.start}:{self.stop or ""}] -> {self.to}'

    def __len__(self):
        return self.stop - self.start

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return [self[i] for i in range(*idx.indices(len(self)))]
        if idx >= len(self):
            raise IndexError
        idx %= len(self)
        return self.to[self.start+idx]

    def __setitem__(self, idx, val):
        if isinstance(idx, slice):
            start, stop, stride = idx.indices(len(self))
            for i, v in zip(range(start, stop, stride), val):
                self[i] = v
            return
        if idx >= len(self):
            raise IndexError(idx)
        idx %= len(self)
        self.to[self.start+idx] = val

    def __getattr__(self, name):
        _ = getattr(self.to, name)

        if name == 'replace_range':
            def wrap(rng, string):
                self.stop = self.start + len(string)
                return _(rng, string)
            
            _ = wrap
            # print(_)

        return _


    def slice(self):
        return self.to[self.start:self.stop].tounicode()
s = String('Hello world')
first, last = s.split_at_mut(5)
assert first.slice() == 'Hello'
assert last.slice() == ' world'
first.replace_range(range(5), 'Screwed')
print(first.slice())
assert first.slice() == 'Screwed'
assert s == 'Screwed world'
# first[0] = 'h'
# first[0] = 'h'
# assert s == 'hello world'