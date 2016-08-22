import random


class Bucket:
    '''Bucket class for storing fingerprints.'''

    def __init__(self, size=4):
        '''
        Initialize bucket.
        
        size : the maximum nr. of fingerprints the bucket can store
            Default size is 4, which closely approaches the best size for FPP between 0.00001 and 0.002 (see Fan et al.).
            If your targeted FPP is greater than 0.002, a bucket size of 2 is more space efficient.
        '''
        self.size = size
        self.b = []

    def insert(self, fingerprint):
        '''
        Insert a fingerprint into the bucket.
        The insertion of duplicate entries is allowed.
        '''
        if not self.is_full():
            self.b.append(fingerprint)
            return True
        return False

    def contains(self, fingerprint):
        return fingerprint in self.b

    def delete(self, fingerprint):
        '''
        Delete a fingerprint from the bucket.

        Returns True if the fingerprint was present in the bucket.
        This is useful for keeping track of how many items are present in the filter.
        '''
        try:
            del self.b[self.b.index(fingerprint)]
            return True
        except ValueError:
            # This error is explicitly silenced.
            # It simply means the fingerprint was never present in the bucket.
            return False

    def swap(self, fingerprint):
        '''
        Swap a fingerprint with a randomly chosen fingerprint from the bucket.
        
        The given fingerprint is stored in the bucket.
        The swapped fingerprint is returned.
        '''
        bucket_index = random.choice(range(len(self.b)))
        fingerprint, self.b[bucket_index] = self.b[bucket_index], fingerprint
        return fingerprint

    def is_full(self):
        return len(self.b) >= self.size

    def __contains__(self, fingerprint):
        return self.contains(fingerprint)

    def __repr__(self):
        return '<Bucket: ' + str(self.b) + '>'

    def __sizeof__(self):
        return super().__sizeof__() + self.b.__sizeof__()