
from timeit import timeit
from string import ascii_letters
from random import shuffle
from functools import partial
from time import time

def split_every(n, l):
    return list(l[i:i+n] for i in range(0, len(l), n))


long_str_tokens = list(ascii_letters * 100) 
shuffle(long_str_tokens)
long_str = ''.join(long_str_tokens)

split_long_str = partial(split_every, l = long_str)

kit = dict (
    e1 = split_long_str(1),
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

    # /timeit(lambda: hash(v), number=10000))

# from array import array

# a = array('u', long_str)

# print(timeit(lambda: a.tounicode(), number=100000), timeit(lambda: ''.join(long_str_tokens), number=100000),)