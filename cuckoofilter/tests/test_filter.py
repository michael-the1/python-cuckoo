import pytest
import cuckoofilter

@pytest.fixture
def cf():
    return cuckoofilter.CuckooFilter(100000, 4)

def test_insert(cf):
    cf.insert('hello')
    assert cf.size == 1

def test_contains(cf):
    cf.insert('hello')
    assert cf.contains('hello'), 'Key was not inserted'

def test_delete(cf):
    cf.insert('hello')
    cf.delete('hello')
    assert not cf.contains('hello'), 'Inserted key was not deleted.'
    assert cf.size == 0, 'Size was not properly kept track of'
