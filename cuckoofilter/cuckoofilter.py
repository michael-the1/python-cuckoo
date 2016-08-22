import bitstring
import mmh3
import random

import bucket


class CuckooFilter:
    '''
    A Cuckoo filter is a data structure for probablistic set-membership queries.
    We can insert items into the filter and, with a very low false positive probability (FPP), ask whether it contains an item or not.
    Cuckoo filters serve as a drop-in replacement for Bloom filters, but are more space-efficient and support deletion of items.

    Cuckoo filters were originally described in:
        Fan, B., Andersen, D. G., Kaminsky, M., & Mitzenmacher, M. D. (2014, December).
        Cuckoo filter: Practically better than bloom.
        In Proceedings of the 10th ACM International on Conference on emerging Networking Experiments and Technologies (pp. 75-88). ACM.

    Their reference implementation in C++ can be found here: https://github.com/efficient/cuckoofilter
    '''

    def __init__(self, capacity, bits_per_fingerprint, bucket_size=4, max_kicks=500):
        '''
        Initialize Cuckoo filter parameters.

        capacity : size of the filter
            Defines how many buckets the filter contains.
        bits_per_fingerprint : nr. of bits per fingerprint
            Defines the size of the fingerprint.
            A larger fingerprint size results in a lower FPP.
            Using 6 bits results in over ~95% load factor, i.e., empirically it is found that the filter is filled over 95% before insertion failure occurs.
        bucket_size : nr. of entries a bucket can hold
            A bucket can hold multiple entries.
            Default size is 4, which closely approaches the best size for FPP between 0.00001 and 0.002 (see Fan et al.).
            If your targeted FPP is greater than 0.002, a bucket size of 2 is more space efficient.
        max_kicks : nr. of times entries are kicked around before deciding the filter is full
            Defaults to 500. This is an arbitrary number also used by Fan et al. and seems reasonable enough.
        '''
        self.capacity = capacity
        self.bits_per_fingerprint = bits_per_fingerprint
        self.max_kicks = max_kicks
        self.buckets = [bucket.Bucket(size=bucket_size) for _ in range(self.capacity)]
        self.size = 0
        self.bucket_size = bucket_size

    def insert(self, item):
        '''
        Inserts a string into the filter.

        Throws an exception if the insertion fails.
        '''
        self.size = self.size + 1
        fingerprint = self.fingerprint(item)
        i1, i2 = self.calculate_index_pair(item, fingerprint)

        if self.buckets[i1].insert(fingerprint):
            return i1
        elif self.buckets[i2].insert(fingerprint):
            return i2

        i = random.choice((i1, i2))
        for kick_count in range(self.max_kicks):
            fingerprint = self.buckets[i].swap(fingerprint)
            i = (i ^ self.index_hash(fingerprint.tobytes())) % self.capacity

            if self.buckets[i].insert(fingerprint):
                return i

        self.size = self.size - 1
        raise Exception('Filter is full')

    def contains(self, item):
        '''Checks if a string was inserted into the filter.'''
        fingerprint = self.fingerprint(item)
        i1, i2 = self.calculate_index_pair(item, fingerprint)
        return (fingerprint in self.buckets[i1]) or (fingerprint in self.buckets[i2])

    def delete(self, item):
        '''Removes a string from the filter.'''
        fingerprint = self.fingerprint(item)
        i1, i2 = self.calculate_index_pair(item, fingerprint)
        if self.buckets[i1].delete(fingerprint) or self.buckets[i2].delete(fingerprint):
            self.size = self.size - 1

    def index_hash(self, item):
        '''Calculate the (first) index of an item in the filter.'''
        item_hash = mmh3.hash_bytes(item)
        index = int.from_bytes(item_hash, byteorder='big') % self.capacity
        return index

    def calculate_index_pair(self, item, fingerprint=None):
        '''Calculate both possible indices for the item'''
        if not fingerprint:
            fingerprint = self.fingerprint(item)
        i1 = self.index_hash(item)
        i2 = (i1 ^ self.index_hash(fingerprint.tobytes())) % self.capacity
        return i1, i2

    def fingerprint(self, item):
        '''
        Takes a string and returns its fingerprint in bits.

        The length of the fingerprint is given by fingerprint_size.
        To calculate this fingerprint, we hash the string with MurmurHash3 and truncate the hash.
        '''
        item_hash = mmh3.hash_bytes(item)
        bits = bitstring.Bits(item_hash)
        bits = bits[:self.bits_per_fingerprint]
        return bits

    def load_factor(self):
        return self.size / (len(self.buckets) * self.bucket_size)

    def __contains__(self, item):
        return self.contains(item)

    def __repr__(self):
        return '<CuckooFilter: capacity=' + str(self.capacity) + ', fingerprint size=' + str(self.bits_per_fingerprint) + ' bits>'

    def __sizeof__(self):
        return super().__sizeof__() + sum(b.__sizeof__() for b in self.buckets)
