# mutable-string

basically a wrapper over array of unicode characters: fast inserts, deletions, replacements, slices, etc. supports all the `str` class methods if does not provide custom implementation itself. works for py3.7+. 

Create:

```python
    from rstring import String
    String() # empty
    String('123') # or String.from_str
    String(array('u', '123')) # or String.from_unicode_array
    String(b'123', encoding='utf8') # or String.from_encoding
    String(str(i) for i in range(1, 5) if i < 4)  # or String.from_iterable
```

Convert back to `str`:
```python
    assert str(String('123')) == '123'
```
It implements (probably) all the magic methods of `str`. And also a bunch of traditional methods:

    char_index, char_indices, chars, clear, contains (__contains__), copy, drain, extend, insert, insert_str, 
    is_empty (!__bool__), lines, map, pop, push, push_str, rchar_index, remove, removeprefix (strip_prefix), 
    removesuffix (strip_suffix), repeat (__mul__), replace_range, retain (filter), rsplit_once, split_at,
    split_inclusive, split_off, split_once, take_from, truncate, __str__ ( as_str to_str), reverse, trim,
    trimr, triml.
Refer to source code and tests for more.

Classmethods:

    __new__, new, from_str, from_iterable, from_unicode_array, from_encoding, from_utf8, has_custom_impl
    
Install:

    pip install git+https://github.com/phantie/mutable-string.git -U
