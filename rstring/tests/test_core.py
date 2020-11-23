import pytest
from .. import String
from ruption import *
from array import array

def test_instance_creation():
    assert str(String()) == ''
    assert str(String.new()) == ''

def test_equality():
    assert String() == String.new() == ''
    assert String.from_str('123') == '123'
    assert String.from_str('me') != String.from_str('you')
    assert String.from_str('-') != '+'

@pytest.fixture
def base():
    return String()

def test_push(base):
    base.push('1')
    base.push('2')
    base.push('3')
    assert str(base) == '123'

def test_push_str(base):
    base.push_str('Hello')
    base.push_str(' ')
    base.push_str('world!')

    assert str(base) == 'Hello world!'

def test_from_str():
    assert str(String.from_str('hello')) == 'hello'
    assert str(String.from_str('')) == ''

def test_length(base):
    def assert_len_is(_: int):
        assert len(base) == _
        assert base.len() == _
        assert base.length == _

    assert_len_is(0)
    base.push_str('hello')
    assert_len_is(5)
    base.push('z')
    assert_len_is(6)

def test_from_utf8():
    assert str(String.from_utf8('hello'.encode('utf-8'))) == 'hello' 

def test_store(base):
    assert isinstance(base.has, array)
    base.push_str('1234')
    assert isinstance(base.has, array)
    assert String.init_store('1234') == array('u', ['1', '2', '3', '4'])
    assert base.has == String.init_store('1234')
    base.push('5')
    assert base.has == String.init_store('12345')
    assert String.from_str('1234').has == String.init_store('1234')

def test_convert_to_str(base):

    method_names = ('__str__', 'as_str', 'to_str')

    assert all(getattr(base, meth)() == '' for meth in method_names)
    base.push_str('123')
    assert all(getattr(base, meth)() == '123' for meth in method_names)
    base.push('4')
    assert all(getattr(base, meth)() == '1234' for meth in method_names)

def test_as_bytes(base):
    assert base.as_bytes('utf-8') == []
    base.push('1')
    assert base.as_bytes('utf-8') == [49]
    base.push_str('23')
    assert base.as_bytes('utf-8') == [49, 50, 51]

def test_truncate(base):
    base.truncate(10)
    assert base == ''
    base.push_str('hello')
    base.truncate(4)
    assert base == 'hell'
    base.truncate(1)
    assert base == 'h'
    base.push_str('ero ain`t ya')
    base.truncate(4)
    assert base == 'hero'

def test_pop(base):
    base.push_str('1234')
    assert base.pop() == some('4')
    assert base.pop() == some('3')
    assert base.pop() == some('2')
    assert base.pop() == some('1')
    assert base.pop() == none

def test_remove(base):
    base.push_str('1234')
    assert base.remove(0) == some('1')
    assert base == '234'
    assert base.remove(1) == some('3')
    assert base == '24'
    assert base.remove(0) == some('2')
    assert base.remove(0) == some('4')
    assert base.remove(0) == none

def test_retain():
    base = String.from_str('f_o_ob_ar')
    base.retain(lambda o: o != '_')
    assert base == 'foobar'

    base = String.from_str('make(something(nice))')
    base.retain(lambda o: o == '(' or o == ')')
    base == '(())'

    base = String.from_str('   #  among   spaces      ')
    base.retain(lambda o: o != ' ')
    base == '#amongspaces'

def test_filter():
    base = String.from_str('sup_#$..er')
    base.filter(lambda o: o.isalpha())
    assert base == 'super'

def test_insert(base):
    base.insert(0, '1')
    base.insert(1, '2')
    assert base == '12'
    base.insert(2, '3')
    assert base == '123'
    with pytest.raises(IndexError):
        base.insert(-1, '4')
    with pytest.raises(IndexError):
        base.insert(100, '4')

def test_insert_str(base):
    base.push_str('123')
    
    base.insert_str(1, '456')
    assert base == '145623'
    base.insert_str(6, '789')
    assert base == '145623789'

def test_falsity(base):
    assert not base
    assert base.is_empty()
    base.push('0')
    assert base
    assert not base.is_empty()

def test_split_off(base):
    base.push_str("Hello, World")
    world = base.split_off(7)
    assert base == "Hello, "
    assert world == "World"

    nothing = world.split_off(5)
    assert nothing == ""
    assert world == "World"

    with pytest.raises(IndexError):
        world.split_off(6)

    all = world.split_off(0)
    assert all == "World"
    assert world == ""

def test_clear(base):
    base.push('c')
    assert base
    base.clear()
    assert not base

def test_drain():
    s = String.from_str("α is alpha, β is beta")
    beta_offset = 12

    t = s.drain(range(beta_offset))
    assert t == "α is alpha, "
    assert s == "β is beta"

def test_replace_range():
    s = String.from_str("α is alpha, β is beta")
    beta_offset = 12

    s.replace_range(range(beta_offset), "Α is capital alpha; ")
    assert s == "Α is capital alpha; β is beta"

    s = String.from_str("12345")
    s.replace_range(range(3), "543")
    assert s == '54345'

    with pytest.raises(TypeError):
        s.replace_range(range(5, -1, -1), "won't work")

def test_map(base):
    assert String.from_str('usa').map(lambda _: _.upper()) == 'USA'
    assert String.from_str('DOWNER').map(lambda _: _.lower()) == 'downer'


def test_split_at_mut():
    pass

def test_chars(base):
    base.push_str('abc')
    assert list(base.chars()) == ['a', 'b', 'c']
    base.push_str('def')
    assert list(base.chars()) == ['a', 'b', 'c', 'd', 'e', 'f']

def test_char_indices(base):
    base.push_str('abcd')
    _ = base.char_indices()
    assert next(_) == (0, 'a')
    assert next(_) == (1, 'b')
    assert next(_) == (2, 'c')
    assert next(_) == (3, 'd')
    with pytest.raises(StopIteration):
        next(_)

# def test_split_whitespace(base):
#     base.push_str("A   few   words")
#     assert base.split_whitespace() == ['A', 'few', 'words']

def test_copy(base):
    new = base.copy()
    base.push_str('update')
    assert new == ''
    assert base == 'update'


def test_from_iterable():
    assert String.from_iterable(('1', '2', '3')) == '123'
    assert String.from_iterable('123') == '123'

def test_from_unicode_array():
    assert String.from_unicode_array(array('u', ('a', 'b'))) == 'ab'
    assert String.from_unicode_array(array('u', '123')) == '123'

def test_extend(base):
    base.extend(('1', '2', '3'))
    assert base == '123'
    base.clear()
    base.extend('some str')
    assert base == 'some str'

def test_addition():
    a1 = String.from_str('yo')
    b1 = String.from_str('ho')
    a2 = 'yo'
    b2 = 'ho'

    assert a1 + a1 == 'yoyo'
    assert a1 + b1 == 'yoho'
    assert a1 + a2 == 'yoyo'
    assert a1 + b2 == 'yoho'
    assert a2 + a1 == 'yoyo'
    assert a2 + b1 == 'yoho'
    assert b2 + a1 == 'hoyo'
    assert b2 + b1 == 'hoho'

    assert isinstance(a1 + a2, String)
    assert isinstance(a2 + a1, String)
    assert isinstance(a1 + a1, String)
    assert isinstance(a2 + b1, String)
    assert isinstance(b2 + b1, String)