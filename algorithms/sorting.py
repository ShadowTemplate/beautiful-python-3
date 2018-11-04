from collections import defaultdict
from math import ceil
from typing import Callable, Dict, List


ItemType = int

def counting_sort(array: List[ItemType], key_fn: Callable[[ItemType], int]) \
    -> List[ItemType]:
    """Counting sort algorithm.
    ref: https://en.wikipedia.org/wiki/Counting_sort
    
    Sort the array according to the values of a key function computed on the 
    items in a stable way.
    It is only suitable in situations where the variation in keys is not 
    significantly greater than the number of items.
    Can be used as a subroutine in other sorting algorithm, such as radix sort.
    
    k := integer such that key_fn(x) <= k, for each x in array
    
    Time complexity analysis:
    Best: O(n+k)
    Average: O(n+k)
    Worst: O(n+k)
    
    Space complexity analysis:
    Best: O(n+k)
    Average: O(n+k)
    Worst: O(n+k)
    """
    
    counts: Dict[int, int] = defaultdict(int)  # frequencies histogram
    k = 0
    for i in array:
        key_value = key_fn(i)
        counts[key_value] += 1
        k = max(k, key_value)
    
    total = 0
    for i in range(k + 1):
        old_count = counts[i]
        counts[i] = total
        total += old_count
        
    sorted_array = array.copy()
    for i in array:
        key_value = key_fn(i)
        sorted_array[counts[key_value]] = i
        counts[key_value] += 1
        
    return sorted_array

