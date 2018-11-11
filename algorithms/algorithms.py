from math import ceil


def median_up_to_5(array, start, end):
    """In-place sort an array of at most 5 items in the range [start, end] via 
    quicksort and return the index of the median.
    If there is an odd number of items return the central index. Otherwise, 
    round upward.
    
    Time complexity analysis:
    Best: O(c), with c a generally negligible constant
    Average: O(c), with c a generally negligible constant
    Worst: O(c), with c a generally negligible constant
    
    Space complexity analysis:
    Best: O(c), with c a generally negligible constant
    Average: O(c), with c a generally negligible constant
    Worst: O(c), with c a generally negligible constant
    """
    
    assert 0 <= start <= end < len(array)
    assert start <= end <= start + 4
    
    quicksort(array, start, end)
    return ceil((end + start) / 2)


def average_pivot(array, start, end):
    """Return a pivot index for the array in the range [start, end].
    
    Time complexity analysis:
    Best: O(1)
    Average: O(1)
    Worst: O(1)
    
    Space complexity analysis:
    Best: O(1)
    Average: O(1)
    Worst: O(1)
    """
    
    assert 0 <= start <= end < len(array)
    
    return (end + start) // 2


def partition(array, start, end, pivot_index):
    """Hoare partition scheme.
    Ref: https://en.wikipedia.org/wiki/Quicksort#Hoare_partition_scheme
    
    In-place partition array items in the range [start, end] into two groups 
    according to a pivot value (< pivot, >= pivot).
    
    Return the final pivot value position.
    
    Time complexity analysis:
    Best: O(n)
    Average: O(n)
    Worst: O(n)
    
    Space complexity analysis:
    Best: O(n)
    Average: O(n)
    Worst: O(n)
    """
    
    assert 0 <= start <= pivot_index <= end < len(array)
    
    pivot_value = array[pivot_index]
    # move pivot value to the end
    array[end], array[pivot_index] = array[pivot_index], array[end]
    
    i, j = start, end
    while i < j:
        # skip items from the left that are in a correct position
        while array[i] < pivot_value:
            i += 1
        # skip items from the right that are in a correct position
        while array[j] >= pivot_value and i < j:
            j -= 1
        if i < j: 
            # swap a left incorrect item with a right incorrect item
            array[i], array[j] = array[j], array[i]
            i += 1
    
    # place pivot between left and right items
    array[j], array[end] = array[end], array[j]
    return j


def quicksort(array, start=None, end=None, pivot_fn=average_pivot):
    """Quicksort algorithm.
    Ref: https://en.wikipedia.org/wiki/Quicksort
    
    In-place sort the items of the array in the range [start, end] by 
    recursively partitioning and sorting them in two subgroups.
    
    Time complexity analysis:
    Best: O(n * log n) if optimal pivot function is chosen
    Average: O(n * log n) if optimal pivot function is chosen
    Worst: O(n^2) if inappropriate pivot function is chosen *
        
    Space complexity analysis:
    Best: O(log n)
    Average: O(log n)
    Worst: O(log n)
    
    *The worst-case time complexity can be improved to O(n log n) by using an 
    appropriate pivot (see median_of_medians_pivot()).
    """
    
    start = 0 if start is None else start
    end = len(array) - 1 if end is None else end
    
    if end <= start:
        return
    
    pivot_index = pivot_fn(array, start, end)
    pivot_index = partition(array, start, end, pivot_index)
    
    # Sedgewick optimization to make sure at most O(log n) space is used
    if pivot_index - 1 - start <= end - pivot_index + 1:  # left part smaller
        quicksort(array, start, pivot_index - 1, pivot_fn)
        quicksort(array, pivot_index + 1, end, pivot_fn)  # tail call
    # right part smaller
    quicksort(array, pivot_index + 1, end, pivot_fn)
    quicksort(array, start, pivot_index - 1, pivot_fn)  # tail call


def quickselect(array, k, pivot_fn=average_pivot):
    """Quickselect algorithm, aka Hoare's selection algorithm.
    Ref: https://en.wikipedia.org/wiki/Quickselect
    
    Return the k-th smallest element in the array.
        
    Time complexity analysis:
    Best: O(n) if optimal pivot function is chosen
    Average: O(n)* if optimal pivot function is chosen
    Worst: O(n^2) if inappropriate pivot function is chosen
    
    Space complexity analysis:
    Best: O(log n)
    Average: O(log n)
    Worst: O(log n)
    
    *Quickselect uses the same approach as quicksort (choose a pivot, partition 
    accordingly, recurse). However, instead of recursing into both sides, as in 
    quicksort, quickselect only recurses into one side (the one with the 
    element it is searching for).
    """

    assert 1 <= k <= len(array)
    
    return array[_quickselect(array, k, pivot_fn, 0, len(array) - 1)]


def _quickselect(array, k, pivot_fn, start, end):
    """Helper function for quickselect algorithm.
    
    Return the index of the k-th smallest element of the array in the range 
    [start, end].
    
    Time/space complexity analysis: see quickselect().
    """
    
    if start == end:
        return start
    
    pivot_index = pivot_fn(array, start, end)
    pivot_index = partition(array, start, end, pivot_index)
    
    if k == pivot_index + 1:
        return pivot_index
    elif k < pivot_index + 1:
        # search in the left half
        return _quickselect(array, k, pivot_fn, start, pivot_index - 1)
    # search in the right half
    return _quickselect(array, k, pivot_fn, pivot_index + 1, end)


def median_of_medians_pivot(array, start, end):
    """Median of medians algorithm.
    Ref: https://en.wikipedia.org/wiki/Median_of_medians
    
    Return the index of an approximate median of the array in the range 
    [start, end] by recursively computing medians of sub-arrays. The 
    approximate median is guaranteed to be between the 30th and 70th 
    percentiles and can be used a good pivot for quicksort and quickselect.
    
    Time/space complexity analysis: see median_of_medians().
    """
    
    # for <= 5 elements just get the index of the median without recursion
    if end - start < 5:
        return median_up_to_5(array, start, end)
    
    # split items in N groups of at most 5 elements, compute the median of each 
    # group and place these values in the first N slots of the array
    for i in range(start, end, 5):
        # shrink the latest subgroup (possibly < 5 items)
        sub_right = min(i + 4, end)
    
        # get the index of the median of the n-th subgroup
        median = median_up_to_5(array, i, sub_right)
        
        # place the median in the right position at the beginning of the array
        new_pos = start + int((i - start) / 5)
        array[median], array[new_pos] = array[new_pos], array[median]
    
    medians_number = ceil((end - start + 1) / 5)  # one for each group
    last_median_pos = start + medians_number - 1
    
    # the median of the medians is the value in the middle of the first N items
    median_of_medians_pos = ceil((start + last_median_pos) / 2)
    return _quickselect(
        array, median_of_medians_pos, median_of_medians_pivot, start, 
        last_median_pos)
     
     
def median_of_medians(array, k):
    """Quickselect algorithm using the approximate median of medians pivot 
    strategy.
    
    Return the k-th smallest element in the array.
    
    Time complexity analysis:
    Best: O(n)
    Average: O(n)
    Worst: O(n)*
    
    Space complexity analysis:
    Best: O(log n)
    Average: O(log n)
    Worst: O(log n)
    
    *The median of medians strategy guarantees to find a pivot value between 
    the 30th and 70th percentiles of the array, thus the search set decreases 
    by at least 30% whenever partitioning. This improves the worst-case time 
    complexity of a general pivot strategy used by quickselect from O(log n) to
    O(n), which is the asymptotically optimal worst-case time complexity of any 
    selection algorithm.
    The median of medians best/average-case time complexities are the same of 
    other pivot strategy, so, in practice, it is usually ignored in favour of 
    others strategies that do not add any overhead while computing pivots.
    """
    
    assert 1 <= k <= len(array)
    
    return quickselect(array, k, median_of_medians_pivot)
