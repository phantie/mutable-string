
from timeit import timeit
from string import ascii_letters
from random import shuffle
from functools import partial

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
