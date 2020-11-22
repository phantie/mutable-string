import pytest
from rstring import String
from array import array

def test_instance_creation():
    assert str(String()) == ''
    assert str(String.new()) == ''

def test_equality():
    assert String() == String.new()
    assert String.from_str('me') != String.from_str('you')
    assert String() != ''

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