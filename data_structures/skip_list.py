from random import random


class NilNode:
    """Sentinel node to indicate the end of the skip list. Its key must be 
    greater than any other internal node key.
    """
    
    def __init__(self, max_key):
        self.key = max_key
        
    def __str__(self):
        return "NIL".format(self.key)
        
    def __repr__(self):
        return "(key: {}, NIL)".format(self.key)


class SkipListNode:
    """Internal node of the skip list containing a value and a key to retrieve 
    it. This key must be smaller than the sentinel node key.
    """
    
    def __init__(self, level, search_key, value):
        self.forward = level * [None]
        self.key = search_key
        self.value = value
        
    def __str__(self):
        return "({}, {})".format(self.key, self.value)
    
    def __repr__(self):
        fw = map(lambda x: "{}: {}".format(x[0], repr(x[1])),
                 enumerate(self.forward))
        return "(key: {}, value: {}, fw: [{}])".format(
            self.key, self.value, ", ".join(fw))


class SkipList:
    """Skip List.
    ref: https://en.wikipedia.org/wiki/Skip_list
    
    A pythonic implementation of the probabilistic data structure presented by 
    William Pugh in the 1990 paper "Skip lists: A probabilistic alternative to 
    balanced trees"
    
    The data structure supports up to max_level levels. In the original paper 
    levels were 1-indexed in the forward array, while here they are 0-indexed. 
    So references of the first level will be found in position 0 of the array, 
    references of the second level will be found in position 1 of the array, 
    and so on (level 1 -> forward[0], level 2 -> forward[1], ...).
    
    The code is kept as similar as possible to the original one, while also 
    trying to add pythonic features, such as generator expressions.
    """
    
    def __init__(self, p, max_level, min_key, max_key):
        """In a skip list, p determines the number of pointers at each level:
        a fraction p of the nodes with level i pointers also have level i + 1 
        pointers. Common values for p are 1/2 and 1/4.
        
        p affects search speed and space requirements of the data structure.
        See the reference paper for further details.
        
        As a rule of thumb, max_level should be L(N), where L(x) is log_(1/p) x
        and N is an upper bound on the number of elements in the list.
        """
        assert 0 < p < 1 <= max_level
        
        self.p = p
        self.max_level = max_level
        self.level = 1
        # create header node
        self.header = SkipListNode(max_level, min_key, None)
        # create sentinel nil node
        nil = NilNode(max_key)
        # set header's forward pointers to sentinel
        for i in range(max_level):
            self.header.forward[i] = nil
            
    def _traverse_list(self, search_key, with_updates):
        """Traverse the skip list from the highest level to the lowest, 
        according to the search key.
        This algorithm corresponds to the policy named "Don't worry, be happy"
        in the original paper.
        
        This routine is used to search, insert and delete values in the list 
        and provides the beautiful time complexity guarantees of the data 
        structure.
        
        Return the node with a key >= of the one in input and, optionally, an
        update array to be used to set new node's references.
        
        Time complexity analysis:
        Best: O(1)
        Average: O(log n)
        Worst: O(log n)
        
        Space complexity analysis:
        Best: O(n)
        Average: O(n)
        Worst: O(n log n)
        """
        
        update = None
        if with_updates:
        # when the search will be completed, update[i] will contain a reference
        # to the rightmost node of level i or higher that is to the left of the
        # location of the deletion
            update = self.max_level * [None]
        
        x = self.header
        for i in reversed(range(self.level)):
            while x.forward[i].key < search_key:
                x = x.forward[i]
            if with_updates:
                update[i] = x
                
            assert x.key < search_key <= x.forward[i].key
        
        x = x.forward[0]
        return x, update
    
    def _get_random_level(self):
        """Return a random level according to the probability distribution
        define by p in the range [1, max_level].
        """
        
        level = 1
        while random() < self.p:
            level += 1
        return min(level, self.max_level)
    
    def search(self, search_key):
        """Return the value associated to a key, if present.
        
        Time/space complexity analysis: see _traverse_list()
        """
        
        x, _ = self._traverse_list(search_key, False)
        return x.value if x.key == search_key else None
        
    def insert(self, search_key, new_value):
        """Insert a new value inside the list in the position defined by the 
        search key. If the key is already present, overwrite the associated
        value.
        
        Time/space complexity analysis: see _traverse_list()
        """
        
        x, update = self._traverse_list(search_key, True)
        if x.key == search_key:  # key present: update its value
            x.value = new_value
            return
        
        # absent key: create a new node and place the new value inside
        new_level = self._get_random_level()
        if new_level > self.level:
            for i in range(self.level, new_level):
                # new levels references will be those of the header in the 
                # range [self.level + 1, new_level] that have been initialized 
                # to point to the special terminating max_key node
                update[i] = self.header
            self.level = new_level
        
        x = SkipListNode(new_level, search_key, new_value)
        for i in range(new_level):
            # x must point to the node at his right
            x.forward[i] = update[i].forward[i]
            # the node preceding x must now point to x
            update[i].forward[i] = x
    
    def delete(self, search_key):
        """Delete the node of the list in the position defined by the search 
        key, if present.
        
        Time/space complexity analysis: see _traverse_list()
        """
        
        x, update = self._traverse_list(search_key, True)        
        if x.key != search_key:  # absent key: nothing to do
            return
        
        # key present: delete the node and update the skip list
        for i in range(self.level):
            if update[i].forward[i] is not x:
                break
            update[i].forward[i] = x.forward[i]
        # x can be garbage collected
        
        # decrease the current level if required
        while self.level > 0 and isinstance(
            self.header.forward[self.level - 1], NilNode):
            self.level -=1

    def _level_generator(self, level=1):
        """Return a generator of the actual list nodes at a certain level of 
        the list, skipping the final sentinel nodes.
        """
        
        assert level <= self.level
        
        x = self.header
        while not isinstance(x, NilNode):
            yield x
            x = x.forward[level - 1]
        
    def __iter__(self):
        """Return a generator of the actual list nodes, by skipping the header
        and the final sentinel nodes.
        """
        
        if self.level == 0:
            return iter([])

        gen = self._level_generator()
        _ = next(gen)  # skip header node
        return gen
    
    def __str__(self):
        return "[{}]".format(", ".join(map(str, self)))
        
    def __repr__(self):
        return "SkipList - p: {}, lev: {}, max-lev: {}, header: {}".format(
            self.p, self.level, self.max_level, repr(self.header))
