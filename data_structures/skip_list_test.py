import random
import unittest

from math import log
from skip_list import SkipList


class TestSkipList(unittest.TestCase):
    
    def test_skip_list(self):
        random.seed(42)
        max_length = 10
        repetitions_per_length = 1000
        int_range = (0, 100)
        min_key = -1
        max_key = 101
        p = 1/2
        
        # generate random lists of integers of variable length
        for length in range(max_length + 1):
            for _ in range(length * repetitions_per_length):
                keys = set()
                skip_list = SkipList(
                    p, int(log(length, 2)) + 3, min_key, max_key)
                
                for _ in range(length):
                    value = random.randint(*int_range)
                    keys.add(value)
                    skip_list.insert(value, value)
                
                # check if items are present in the same order
                array = [(k, k) for k in keys]
                array.sort()
                
                self.assertEqual(
                    str(array), str(skip_list), 
                    "List possibly not sorted: {}".format(skip_list))
                
                # delete every value
                for k in keys:
                    self.assertEqual(
                        k, skip_list.search(k),
                        "Error while searching key {} in {}".format(
                            k, skip_list))
                    skip_list.delete(k)
                
                # check search fails after deletion
                for k in keys:
                    self.assertIsNone(
                        skip_list.search(k), 
                        "Error after deleting key {} in {}".format(
                            k, skip_list))
                
                # check if list is empty
                self.assertEqual(
                    str([]), str(skip_list), "List not empty: {}".format(
                        skip_list))


if __name__ == "__main__":
    unittest.main()



