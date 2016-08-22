import random


class Bucket:

    def __init__(self, size=4):
        self.size = size
        self.b = []

    def insert(self, fingerprint):
        if not self.is_full():
            self.b.append(fingerprint)
            return True
        return False

    def contains(self, fingerprint):
        return fingerprint in self.b

    def delete(self, fingerprint):
        try:
            del self.b[self.b.index(fingerprint)]
        except ValueError:
            pass

    def swap(self, fingerprint):
        bucket_index = random.choice(range(len(self.b)))
        fingerprint, self.b[bucket_index] = self.b[bucket_index], fingerprint
        return fingerprint

    def is_full(self):
        return len(self.b) >= self.size

    def __contains__(self, fingerprint):
        return self.contains(fingerprint)

    def __repr__(self):
        return '<Bucket: ' + str(self.b) + '>'
