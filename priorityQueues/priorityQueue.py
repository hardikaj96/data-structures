from linkedlists.positionallist import PositionalList
class PriorityQueueBase:
    """Abstract base class for a priority queue"""

    class Item:
        """Lightweight composite to store priority queue items"""

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __lt__(self, other):
            return self.key < other.key

    def is_empty(self):
        """Return True if the priority Queue is empty"""
        return len(self) == 0

class UnsortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with an unsorted list"""

    def find_min(self):
        """Return Position of item with minimum key"""
        if self.is_empty():
            raise Exception('Priority queue is empty')
        small = self.data.first()
        walk = self.data.after(small)
        while walk is not None:
            if walk.element() < small.element():
                small = walk
            walk = self.data.after(walk)
        return small

    def __init__(self):
        """Create a new empty Priority Queue"""
        self.data = PositionalList()

    def __len__(self):
        """Return the number of items in the priority queue"""
        return len(self.data)

    def add(self, key, value):
        """Add a key-value pair."""
        self.data.add_last(self.Item(key, value))

    def min(self):
        """Return but do not remove (k,v) tuple with minimum key"""
        p = self.find_min()
        item = p.element()
        return (item.key, item.value)

    def remove_min(self):
        """Remove and return (k,v) tuple with minimum key"""
        p = self.find_min()
        item = self.data.delete(p)
        return (item.key, item.value)

class SortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a sorted list"""

    def __init__(self):
        """Create a new empty Priority Queue"""
        self.data = PositionalList()

    def __len__(self):
        """Return the number of items in the Priority Queue"""
        return len(self.data)

    def add(self, key, value):
        """Add a key-value pair"""
        newest = self.Item(key, value)
        walk = self.data.last()
        while walk is not None and newest < walk.element():
            walk = self.data.before(walk)
        if walk is None:
            self.data.add_first(newest)
        else:
            self.data.add_after(walk, newest)

    def min(self):
        """Return but do not remove (k,v) tuple with minimum key"""
        if self.is_empty():
            raise Exception('Priority queue is empty')
        p = self.data.first()
        item = p.element()
        return (item.key, item.value)

    def remove_min(self):
        """Remove and return (k,v) tuple with minimum key"""
        if self.is_empty():
            raise Exception('Priority queue is empty')
        item = self.data.delete(self.data.first())
        return (item.key, item.value)

class HeapPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with a binary heap"""

    def parent(self, j):
        return (j-1) // 2

    def left(self, j):
        return 2*j + 1

    def right(self, j):
        return 2*j + 2

    def has_left(self, j):
        return self.left(j) < len(self.data)

    def has_right(self, j):
        return self.right(j) < len(self.data)

    def swap(self, i, j):
        """Swap the elements at indices i and j of array"""
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def upheap(self, j):
        parent = self.parent(j)
        if j>0 and self.data[j]<self.data[parent]:
            self.swap(j, parent)
            self.upheap(parent)

    def downheap(self, j):
        if self.has_left(j):
            left = self.left(j)
            small_child = left
            if self.has_right(j):
                right = self.right(j)
                if self.data[right] < self.data[left]:
                    small_child = right
            if self.data[small_child] < self.data[j]:
                self.swap(j, small_child)
                self.downheap(small_child)

    def __init__(self):
        """Create a new empty Priority Queue"""
        self.data = []

    def __len__(self):
        """Return the number of items in the priority queue"""
        return len(self.data)

    def add(self, key, value):
        """Add a key-value pair to the priority queue"""
        self.data.append(self.Item(key, value))
        self.upheap(len(self.data)-1)

    def min(self):
        """Return but do not remove (k,v) tuple with minimum key"""
        if self.is_empty():
            raise Exception('Priority Queue is empty')
        item = self.data[0]
        return (item.key, item.value)

    def remove_min(self):
        """Remove and return (k,v) tuple with minimum key"""
        if self.is_empty():
            raise Exception('Priority queue is empty')
        self.swap(0, len(self.data)-1)
        item = self.data.pop()
        self.downheap(0)
        return (item.key, item.value)

class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """A locator based priority queue implemented with a binary heap"""

    class Locator(HeapPriorityQueue.Item):

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self.index = j

        def swap(self, i, j):
            super().swap(i, j)
            self.data[i].index = i
            self.data[j].index = j

        def bubble(self, j):
            if j>0 and self.data[j] < self.data[self.parent(j)]:
                self.upheap(j)
            else:
                self.downheap(j)

        def add(self, key, value):
            """Add a key-value pair"""
            token = self.Locator(key, value, len(self.data))
            self.data.append(token)
            self.upheap(len(self.data)-1)
            return token

        def update(self, loc, newkey, newval):
            """Update the key and value for the entry identified by Locator loc"""
            j = loc.index
            if not (0 <= j < len(self) and self.data[j] is loc):
                raise ValueError('Invalid Locator')
            loc.key = newkey
            loc.value = newval
            self.bubble(j)

        def remove(self, loc):
            """Remove and return the (k,v) pair identified by Locator loc"""
            j = loc.index
            if not (0 <= j < len(self) and self.data[j] is loc):
                raise ValueError('Invalid locator')
            if j == len(self) - 1:
                self.data.pop()
            else:
                self.swap(j, len(self)-1)
                self.data.pop()
                self.bubble(j)
            return (loc.key, loc.value)
