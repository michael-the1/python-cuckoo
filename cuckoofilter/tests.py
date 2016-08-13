import unittest
import cuckoofilter

class TestCuckooFilter(unittest.TestCase):

    def setUp(self):
        self.cf = cuckoofilter.CuckooFilter(1000000, 4)

    def test_insert(self):
        self.cf.insert('hello')
        self.assertEquals(self.cf.size, 1)

    def test_contains(self):
        self.cf.insert('hello')
        self.assertTrue(self.cf.contains('hello'), 'Key was not inserted')

    def test_delete(self):
        self.cf.insert('hello')
        self.cf.delete('hello')
        self.assertFalse(self.cf.contains('hello'), 'Inserted key was not deleted.')

if __name__ == '__main__':
    unittest.main()
