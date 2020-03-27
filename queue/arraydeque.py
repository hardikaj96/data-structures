class ArrayDeque:
    """Double Ended Queue Implementation using Python lists"""
    DEFAULT_CAPACITY = 10

    def __init__(self):
        """Initialize empty list as deque."""
        self.data = [None] * ArrayDeque.DEFAULT_CAPACITY
        self.first = 0
        self.last = 0
        self.size = 0

    def __len__(self):
        """Return the number of elements in deque D"""
        return self.size

    def is_empty(self):
        """Returns True if the deque is empty."""
        return self.size == 0

    def first_element(self):
        """Return the first element of deque D
        Raise an Empty exception if deque is empty"""
        if self.is_empty():
            raise Exception("Deque is empty")
        return self.data[self.first]

    def last_element(self):
        """Return the last element of deque D
        Raise an Empty exception if deque is empty"""
        if self.is_empty():
            raise Exception("Deque is empty")
        return self.data[self.last]

    def add_first(self, element):
        """ Add an element to the front of the deque"""
        if self.size == len(self.data):
            self.resize(2 * len(self.data))
        if self.size == 0:
            self.data[self.first] = element
        else:
            self.first = (self.first - 1) % len(self.data)
            self.data[self.first] = element
        self.size += 1

    def add_last(self, element):
        """ Add an element to the end of the deque"""
        if self.size == len(self.data):
            self.resize(2 * len(self.data))
        if self.size == 0 and self.first == self.last:
            self.data[self.last] = element
        else:
            self.last = (self.last + 1) % len(self.data)
            self.data[self.last] = element
        self.size += 1

    def delete_first(self):
        """Remove and return the first element from deque D
        Raise an Empty error is the deque is empty"""
        if self.is_empty():
            raise Exception('Deque is empty')
        answer = self.data[self.first]
        self.data[self.first] = None
        if self.size == 1:
            self.size -= 1
            return answer
        self.first = (self.first + 1) % len(self.data)
        self.size -= 1
        return answer

    def delete_last(self):
        """Remove and return the last element from deque D
        Raise an Empty error is the deque is empty"""
        if self.is_empty():
            raise Exception('Deque is empty')
        answer = self.data[self.last]
        self.data[self.last] = None
        if self.size == 1:
            self.size -= 1
            return answer
        self.last = (self.last - 1) % len(self.data)
        self.size -= 1
        return answer

    def resize(self, cap):
        """Resize to a new capacity >= len(self"""
        old = self.data
        self.data = [None] * cap
        walk = self.first
        for k in range(self.size):
            self.data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self.first = 0
        self.last = len(self.data) - 1
