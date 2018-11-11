from hashlib import md5
from itertools import chain
from typing import Callable, List
from BitVector import BitVector


FilterItem = str

class BloomFilter:
    """"Bloom Filter.
    ref: https://en.wikipedia.org/wiki/Bloom_filter
    
    For a given false positive probability p, the length of a Bloom filter m is 
    proportionate to the number of elements being filtered n:
    m = -(n*log p)/(log2 2)^2 
    The required number of hash functions k only depends on the target p:
    k = -log2 p
    For a given m and n, the k that minimizes p is:
    k = (m/n)*log 2
    """

    def __init__(self, m: int, *hash_fns: Callable[[FilterItem], int]):
        assert m > 0
        
        self.m = m
        # initialize a bit vector of size m with all 0s
        self.bits = BitVector(intVal=0, size=m)  # type: ignore
        self.hash_fns = list(hash_fns)
        
        assert len(self.hash_fns) > 0
    
    def add(self, item: FilterItem) -> None:
        """Time complexity analysis:
        Best: O(k)
        Average: O(k)
        Worst: O(k)
        
        Space complexity analysis:
        Best: O(m)
        Average: O(m)
        Worst: O(m)
        """
        
        for hf in self.hash_fns:
            self.bits[hf(item) % self.m] = 1
    
    def __contains__(self, item: FilterItem) -> bool:
        """Probability of false positive circa (1-e^(-kn/m))^k
        
        Time complexity analysis:
        Best: O(1)
        Average: O(k)
        Worst: O(k)
        
        Space complexity analysis:
        Best: O(m)
        Average: O(m)
        Worst: O(m)
        """
        
        res: bool = all(map(lambda hf: self.bits[hf(item) % self.m], self.hash_fns))
        return res


def md5_to_int(item: FilterItem) -> int:
    return int(md5(item.encode('utf-8')).hexdigest(), 16)


def main() -> None:
    bloom_filter = BloomFilter(13, md5_to_int)
    present_values: List[FilterItem] = ["these", "values", "are", "ok"]
    absent_values: List[FilterItem] = ["---", "but", "those", "should", "not"]
    
    for i in present_values:
        bloom_filter.add(i)
    
    for i in present_values:
        print("Item '{}'\tExpected: {}\tFound: {}".format(
            i, True, i in bloom_filter))
        # Item 'these'    Expected: True  Found: True
        # Item 'values'   Expected: True  Found: True
        # Item 'are'      Expected: True  Found: True
        # Item 'ok'       Expected: True  Found: True
    
    for i in absent_values:
        print("Item '{}'\tExpected: {}\tFound: {}".format(
            i, False, i in bloom_filter))
        # Item '---'      Expected: False Found: False
        # Item 'but'      Expected: False Found: True
        # Item 'those'    Expected: False Found: False
        # Item 'should'   Expected: False Found: False
        # Item 'not'      Expected: False Found: True


if __name__ == "__main__":
    main()
