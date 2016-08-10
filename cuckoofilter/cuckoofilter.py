import hashlib
import bitstring


class CuckooFilter:
    '''
    A Cuckoo Filter is data structure for probablistic set-membership queries.
    With a very low false positive probability (FPP), we can ask whether it contains an item or not.
    Cuckoo Filters serve as a drop-in replacement for Bloom filters, but are more space-efficient and support deletion of items.

    Cuckoo Filters were originally described in a paper by B. Fan, D. Andersen, M. Kaminsky, and M. Mitzenmacher (2014).
    Their reference implementation in C++ can be found here: https://github.com/efficient/cuckoofilter
    '''

    def __init__(self, capacity, bits_per_fingerprint, bucket_size=4, max_kicks=500):
        '''
        Initialize Cuckoo Filter parameters.

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
        self.bucket_size = bucket_size
        self.max_kicks = max_kicks
        self.buckets = []

    def insert(self, item):
        '''
        Inserts an integer into the filter.

        Throws an exception if the insertion failed.
        '''

    def contains(self, item):
        '''Checks if an integer was inserted into the filter.'''

    def delete(self, item):
        '''Removes an integer from the filter.'''

    @staticmethod
    def fingerprint(item, fingerprint_size):
        '''
        Takes an integer and returns its fingerprint in bits.

        The length of the fingerprint is given by fingerprint_size.
        To calculate this fingerprint, we hash the integer with sha1 and truncate the hash.
        '''
        hash_object = hashlib.sha1(bytes(item))
        bits = bitstring.Bits(hash_object.digest())
        bits = bits[:fingerprint_size]
        return bits
