import random
import unittest

from algorithms import median_of_medians, partition, quickselect, quicksort


class TestPartition(unittest.TestCase):
    
    def test_partition(self):
        array = []
        with self.assertRaises(AssertionError):
            partition(array, 0, 0, 0)
            
        array = [1]
        partitioning = [1]
        k = partition(array, 0, 0, 0)  # partition by 1 the only item
        self.assertEqual(
            k, 0, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 2]
        partitioning = [1, 2]
        k = partition(array, 0, 1, 0)  # partition by 1 all the array
        self.assertEqual(
            k, 0, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 2]
        partitioning = [1, 2]
        k = partition(array, 0, 1, 1)  # partition by 2 all the array
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [2, 1]
        partitioning = [2, 1]
        k = partition(array, 0, 0, 0)  # partition by 2 the first item
        self.assertEqual(
            k, 0, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [2, 1]
        partitioning = [2, 1]
        k = partition(array, 1, 1, 1)  # partition by 1 the last item
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 3, 2]
        partitioning = [1, 2, 3]
        k = partition(array, 0, 2, 1)  # partition by 3 all the array
        self.assertEqual(
            k, 2, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 3, 2]
        partitioning = [1, 2, 3]
        k = partition(array, 0, 2, 2)  # partition by 2 all the array
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 3, 2]
        partitioning = [1, 3, 2]
        k = partition(array, 0, 2, 0)  # partition by 1 all the array
        self.assertEqual(
            k, 0, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [2, 1, 3]
        partitioning = [2, 1, 3]
        k = partition(array, 0, 2, 2)  # partition by 3 all the array
        self.assertEqual(
            k, 2, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [3, 2, 1]
        partitioning = [2, 3, 1]
        k = partition(array, 0, 1, 0)  # partition by 3 the first two items
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [3, 2, 1]
        partitioning = [3, 1, 2]
        k = partition(array, 1, 2, 2)  # partition by 1 the last two items
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 4, 2, 3]
        partitioning = [1, 2, 3, 4]
        k = partition(array, 0, 3, 3)  # partition by 3 all the array
        self.assertEqual(
            k, 2, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 4, 2, 3]
        partitioning = [1, 2, 3, 4]
        k = partition(array, 0, 3, 2)  # partition by 2 all the array
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [1, 4, 2, 3]
        partitioning = [1, 2, 4, 3]
        k = partition(array, 0, 2, 2)  # partition by 2 the first three items
        self.assertEqual(
            k, 1, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))
        
        array = [7, 5, 3, 4, 2, 6]
        partitioning = [2, 3, 4, 6, 7, 5]
        k = partition(array, 0, 5, 3)  # partition by 4 all the array
        self.assertEqual(
            k, 2, 
            "Wrong partition index {} in {}".format(k, array))
        self.assertEqual(
            array, partitioning, 
            "Wrong partitioning: {} vs {}".format(array, partitioning))


class TestQuicksort(unittest.TestCase):
    
    def test_quicksort(self):
        random.seed(42)
        max_length = 10
        repetitions_per_length = 1000
        int_range = (-50, 50)
        
        # generate random lists of integers of variable length
        for length in range(max_length + 1):
            for _ in range(length * repetitions_per_length):
                array = [random.randint(*int_range) for _ in range(length)]
                array_copy = array.copy()
                quicksort(array)
                array_copy.sort()
                self.assertEqual(
                    array, array_copy, 
                    "Error while sorting {}".format(array))


class TestQuickselect(unittest.TestCase):
    
    def test_quickselect(self):
        random.seed(42)
        max_length = 10
        repetitions_per_length = 1000
        int_range = (-50, 50)
        
        with self.assertRaises(AssertionError):
            quickselect([1], 0)  # test 0 position
            
        with self.assertRaises(AssertionError):
            quickselect([1], 2)  # test exceeding position
        
        # generate random lists of integers of variable length
        for length in range(max_length + 1):
            for _ in range(length * repetitions_per_length):
                for j in range(1, length + 1):  # test every position
                    array = [random.randint(*int_range) for _ in range(length)]
                    array_copy = array.copy()
                    array_copy.sort()
                    self.assertEqual(
                        quickselect(array, j), array_copy[j - 1],
                        "Error while picking {}-th minimum from {}".format(
                            j, array))


class TestMedianOfMedians(unittest.TestCase):
    
    def test_median_of_medians(self):
        random.seed(42)
        max_length = 10
        repetitions_per_length = 1000
        int_range = (-50, 50)
        
        with self.assertRaises(AssertionError):
            median_of_medians([1], 0)  # test 0 position
            
        with self.assertRaises(AssertionError):
            median_of_medians([1], 2)  # test exceeding position
        
        # generate random lists of integers of variable length
        for length in range(max_length + 1):
            for _ in range(length * repetitions_per_length):
                for j in range(1, length + 1):  # test every position
                    array = [random.randint(*int_range) for _ in range(length)]
                    array_copy = array.copy()
                    array_copy.sort()
                    self.assertEqual(
                        median_of_medians(array, j), array_copy[j - 1],
                        "Error while picking {}-th minimum from {}".format(
                            j, array))


if __name__ == "__main__":
    unittest.main(verbosity=2)
