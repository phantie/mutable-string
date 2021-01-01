import pytest
from .. import String
from ruption import *
from array import array
from take import take

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
    usa = String.from_str('usa')
    usa.map(lambda _: _.upper())
    assert usa == 'USA'

    DOWNER = String.from_str('DOWNER')
    DOWNER.map(lambda _: _.lower())
    assert DOWNER == 'downer'


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

def test_convenient_creation():
    # String.from_str
    assert String('123') == '123'
    assert String(f'{str.__name__}') == 'str'
    
    # String.from_unicode_array
    assert String(array('u', '123')) == '123'
    assert String(array('u', ['a', 'b', 'c'])) == 'abc'

    # String.from_encoding
    assert String(b'123', encoding = 'utf8') == '123'
    assert String(b'\xff\xfe1\x002\x003\x00', 'utf16') == '123'

    # String.from_iterable
    assert String(iter('1090')) == '1090'
    assert String((str(i) for i in range(7) if i%2)) == '135'

def test_strip_prefix():
    s = String('foofoo')
    s.strip_prefix('foo')
    assert s == 'foo'

    s = String('foo' * 10 + 'boo')
    s.strip_prefix('foo', recurr=True)
    assert s == 'boo'

    s = String('bar:foo')
    s.strip_prefix('bar:')
    assert s == 'foo'

    s = String('bar:foo')
    s.strip_prefix('baz:')
    assert s == 'bar:foo'

    s = String('bar:foo')
    s.strip_prefix('baz:123456')
    assert s == 'bar:foo'

    s = String('123')
    s.strip_prefix('123')
    assert s == ''

    s = String('123123123123some')
    s.strip_prefix('123', recurr=True)
    assert s == 'some'
    
    s = String('123')
    s.strip_prefix('')
    assert s == '123'

def test_strip_suffix():
    s = String('foofoo')
    s.strip_suffix('foo')
    assert s == 'foo'

    s = String('foofoo1')
    s.strip_suffix('foo')
    assert s == 'foofoo1'
    
    s = String('123')
    s.strip_suffix('123456')
    assert s == '123'

    s = String('1234567890abcabc')
    s.strip_suffix('abc')
    assert s == '1234567890abc'

    s = String('1234567890abcabc')
    s.strip_suffix('abc', recurr=True)
    assert s == '1234567890'

    s = String('123')
    s.strip_suffix('123')
    assert s == ''

    s = String('123')
    s.strip_suffix('')
    assert s == '123'


def test_multiply():
    assert String('123') * 3 == '123' * 3
    assert 3 * String('123') == '123' * 3
    assert 10 * String() == ''
    assert String('1').repeat(3) == '111'

def test_has_custom_impl():
    assert String.has_custom_impl('removeprefix')
    assert String.has_custom_impl('removesuffix')

def test_split_at():
    assert String('mice').split_at(2) == ('mi', 'ce')
    assert String('12345').split_at(3) == ('123', '45')

def test_lines():
    assert String('foo\r\nbar\n\nbaz\n').lines() == ['foo', 'bar', '', 'baz']
    assert String('foo\nbar\n\r\nbaz').lines() == ['foo', 'bar', '', 'baz']
    assert String('foo\nbar\n\r\nbaz\n\x20\x20').lines() == ['foo', 'bar', '', 'baz', '  ']

def test_in():
    assert '123' in String('asdas123123a')
    assert String('123') in String('asdas123123a')
    assert array('u', '123') in String('asdas123123a')
    assert String('asdas123123a').contains('123')

def test_split_inclusive():
    assert list(String('123\n345\n678\n').split_inclusive('\n')) == ['123\n', '345\n', '678\n']
    assert list(String('123\n345\n678').split_inclusive('\n')) == ['123\n', '345\n', '678']
    assert list(String('aaaaa').split_inclusive('b')) == ['aaaaa']
    assert list(String().split_inclusive('Q')) == []
    assert list(String(' ').split_inclusive('Q')) == [' ']
    with pytest.raises(AssertionError):
        String().split_inclusive('two_more_syms')

def test_collect():
    assert String('123').collect(str) == '123'
    assert String('123').collect(list) == ['1', '2', '3']
    assert String('123').collect(tuple) == ('1', '2', '3')

def test_char_index():
    assert String('123').char_index('2') == some(1)
    assert String('123').char_index('3') == some(2)
    assert String('123').char_index('4') == none

def test_char_rindex():
    assert String('123123').rchar_index('2') == some(4)
    assert String('123123').rchar_index('3') == some(5)
    assert String('123123').rchar_index('4') == none

def test_split_once():
    assert String('123').split_once('1') == some(('', '23'))
    assert String('123').split_once('2') == some(('1', '3'))
    assert String('123').split_once('3') == some(('12', ''))
    assert String('123').split_once('4') == none

def test_rsplit_once():
    assert String('123123').rsplit_once('1') == some(('123', '23'))
    assert String('123123').rsplit_once('2') == some(('1231', '3'))
    assert String('123123').rsplit_once('3') == some(('12312', ''))
    assert String('123123').rsplit_once('4') == none

def test_reverse():
    assert take(String('1234')).reverse().unwrap() == '4321'
    assert take(String('abc')).reverse().unwrap() == 'cba'
    assert take(String('')).reverse().unwrap() == ''
    assert take(String('121')).reverse().unwrap() == '121'

def test_trim():
    _ = '   a b c  '
    assert take(String(_)).trim().unwrap() == 'a b c'
    assert take(String(_)).trimr().unwrap() == '   a b c'
    assert take(String(_)).triml().unwrap() == 'a b c  '
    _ = ''
    assert take(String(_)).trim().unwrap() == ''
    assert take(String(_)).trimr().unwrap() == '' 
    assert take(String(_)).triml().unwrap() == ''

def test_bool():
    assert String('123')
    assert not String('')

def test_comp():
    a, b = '123', '4567'
    assert (a < b) == (String(a) < String(b)) == (String(a) < b) == (a < String(b))
    a, b = 'fdhdfh', 'dshfg'
    assert (a > b) == (String(a) > String(b)) == (String(a) > b) == (a > String(b))
    a, b = '123qwe', 'qwe123'
    assert (a <= b) == (String(a) <= String(b)) == (String(a) <= b) == (a <= String(b))
    a, b = 'zx1c', 'zx2c'
    assert (a >= b) == (String(a) >= String(b)) == (String(a) >= b) == (a >= String(b))

def test_trim_num():
    assert take(String('123')).trim_num(0).unwrap() == '123'
    assert take(String('123')).trim_num(1).unwrap() == '2'
    assert take(String('123')).trim_num(2).unwrap() == ''
    
    assert take(String('123')).trimr_num(0).unwrap() == '123'
    assert take(String('123')).trimr_num(1).unwrap() == '12'
    assert take(String('123')).trimr_num(2).unwrap() == '1'
    assert take(String('123')).trimr_num(3).unwrap() == ''
    assert take(String('123')).trimr_num(4).unwrap() == ''

    assert take(String('123')).triml_num(0).unwrap() == '123'
    assert take(String('123')).triml_num(1).unwrap() == '23'
    assert take(String('123')).triml_num(2).unwrap() == '3'
    assert take(String('123')).triml_num(3).unwrap() == ''
    assert take(String('123')).triml_num(4).unwrap() == ''

