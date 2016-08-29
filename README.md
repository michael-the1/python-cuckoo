# python-cuckoo
```python-cuckoo``` is an implementation of a Cuckoo filter in python 3.

Cuckoo filters serve as a drop-in replacement for Bloom filters.
Just like Bloom filters, we can add items to the filter and then ask the filter whether that item is in the filter or not.
Just like Bloom filters, there is a (very small and tunable) chance this will return a false positive.
Unlike regular Bloom filters, Cuckoo filters also support deletion of items.
Cuckoo filters use less space than Bloom filters for low false positive rates.

# Usage

```python
>>> import cuckoofilter
>>> cf = cuckoofilter.CuckooFilter(capacity=100000, fingerprint_size=1)

>>> cf.insert('Bin Fan')
66349

>>> cf.contains('Bin Fan')
True

>>> cf.contains('Michael The')
False

>>> cf.delete('Bin Fan')
True

>>> cf.contains('Bin Fan')
False
```

# Why use Cuckoo filters
The short answer: if you don't know whether you should use a Bloom filter or a Cuckoo filter, use a Cuckoo filter.
For a well-written and visual explanation, check out [Probabilistic Filters By Example](https://bdupras.github.io/filter-tutorial/).

Cuckoo filters are very similar to Bloom filters.
They are both great at reducing a disk queries.
Some example usages of Bloom filters:
- Checking whether a URL is malicious or not ([Google Chrome](http://blog.alexyakunin.com/2010/03/nice-bloom-filter-application.html))
- Deciding whether an item should be cached or not ([Akamai](http://dl.acm.org/citation.cfm?doid=2805789.2805800))
- Keep track of what articles a user has already read ([Medium](https://medium.com/blog/what-are-bloom-filters-1ec2a50c68ff#.xlkqtn1vy))

# Why not use Cuckoo filters
As a Cuckoo filter is filled up, insertion will become slower as more items need to be "kicked" around.
If your application is sensitive to timing on insertion, choose a different data structure.

Cuckoo filters might reject insertions.
This occurs when the filter is about to reach full capacity or a fingerprint is inserted more than 2b times, where b is the bucket size.
This limitation is also present in Counting Bloom filters.
If this limitation is unacceptable for your application, use a different data structure.

# Testing & profiling
Python-cuckoo comes with a test suite (```cuckoofilter/tests/```).
We recommend using [```py.test```](http://pytest.org/) to run unit tests.

```
pip install pytest
pytest cuckoofilter/
```

To generate a test coverage report, install the pytest coverage plugin and generate an html report.

```
pip install pytest-cov
pytest --cov-report html cuckoofilter/
```

The report will be created in a folder called ```htmlcov```.
Open ```htmlcov/index.html``` to inspect what parts of the library are tested.

To find out what parts of the library are slow, we need to profile our library.
To do this, we can use ```cProfile``` by running ```python -m cProfile example.py```.
For a visualization of this profiling information, we can use [snakeviz](https://jiffyclub.github.io/snakeviz/).

```
pip install snakeviz
python -m cProfile -o out.profile example.py
snakeviz out.profile
```

# Original paper

Cuckoo filters were first described in:

>Fan, B., Andersen, D. G., Kaminsky, M., & Mitzenmacher, M. D. (2014, December).  
>Cuckoo filter: Practically better than bloom.  
>In Proceedings of the 10th ACM International on Conference on emerging Networking Experiments and Technologies (pp. 75-88). ACM.

Their reference implementation in C++ can be found on [github](https://github.com/efficient/cuckoofilter).

## See also

- [Probablistic Filters By Example](https://bdupras.github.io/filter-tutorial/) for a well-written and visual explanation of Cuckoo filters vs. Bloom filters.
- [Cuckoo Filters](http://mybiasedcoin.blogspot.nl/2014/10/cuckoo-filters.html) — blog post by M. Mitzenmacher, the fourth author of the original paper.
- [Cuckoo Filter implementation in java](https://github.com/bdupras/guava-probably)
- [Cuckoo Filter implementation in Go](https://github.com/irfansharif/cfilter)
