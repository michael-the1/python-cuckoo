import pytest
import cuckoofilter

@pytest.fixture
def bucket():
    return cuckoofilter.Bucket()

def test_initialization(bucket):
    assert bucket.size == 4
    assert bucket.b == []

def test_insert(bucket):
    assert bucket.insert('hello')

def test_insert_full(bucket):
    for i in range(bucket.size):
        bucket.insert('a')
    assert not bucket.insert('a')

def test_contains(bucket):
    bucket.insert('hello')
    assert bucket.contains('hello')

def test_delete(bucket):
    bucket.insert('hello')
    assert bucket.delete('hello')
    assert not bucket.contains('hello')

def test_delete_non_existing_fingerprint(bucket):
    assert not bucket.delete('hello')

def test_swap(bucket):
    bucket.insert('hello')
    swapped_fingerprint = bucket.swap('world')
    assert swapped_fingerprint == 'hello'
    assert bucket.contains('world')

def test_is_full(bucket):
    for i in range(4):
        bucket.insert(i)
    assert bucket.is_full()
