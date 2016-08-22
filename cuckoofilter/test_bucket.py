import unittest
import bucket

class TestBucket(unittest.TestCase):

    def setUp(self):
        self.b = bucket.Bucket()

    def test_initialization(self):
        self.assertEqual(self.b.size, 4)
        self.assertEqual(self.b.b, [])

    def test_insert(self):
        self.b.insert('hello')

    def test_contains(self):
        self.b.insert('hello')
        self.assertTrue(self.b.contains('hello'))

    def test_delete(self):
        self.b.insert('hello')
        self.b.delete('hello')
        self.assertFalse(self.b.contains('hello'))

    def test_swap(self):
        self.b.insert('hello')
        swapped_fingerprint = self.b.swap('world')
        self.assertEqual(swapped_fingerprint, 'hello')
        self.assertTrue(self.b.contains('world'))

    def test_is_full(self):
        for i in range(4):
            self.b.insert(i)
        self.assertTrue(self.b.is_full())

if __name__ == '__main__':
    unittest.main()
