import random
import unittest

from collections import Counter
from sorting import counting_sort


class TestCountingSort(unittest.TestCase):
    
    def test_counting_sort(self):
        random.seed(42)
        max_length = 10
        repetitions_per_length = 1000
        int_range = (0, 100)
        
        # test sort with identity key function
        id_fn = lambda x: x
        
        # generate random lists of integers of variable length
        for length in range(max_length + 1):
            for _ in range(length * repetitions_per_length):
                array = [random.randint(*int_range) for _ in range(length)]
                count_sorted = counting_sort(array, id_fn)
                sorted_array = array.sort()
                self.assertEqual(
                    array, count_sorted, 
                    "Error while sorting {}".format(array))

        # test sort with mod key function
        mod3_fn = lambda x: x % 3
        
        # generate random lists of integers of variable length
        for length in range(max_length + 1):
            for _ in range(length * repetitions_per_length):
                array = [random.randint(*int_range) for _ in range(length)]
                count_sorted = counting_sort(array, mod3_fn)
                # groups items by their mod 3 values
                groups = []
                for n in range(3):
                    groups.append([i for i in array if mod3_fn(i) == n])
    
                # check if the sorted array contains the group values in order
                start_index = 0
                for g in groups:
                    end_index = start_index + len(g)
                    slice_count = Counter(count_sorted[start_index: end_index])
                    self.assertEqual(
                        Counter(g), slice_count,
                        "Error while sorting {}.\nWrong items: {}".format(
                            array, slice_count))
                    start_index = end_index


if __name__ == "__main__":
    unittest.main(verbosity=2)
