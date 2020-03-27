class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage"""
    DEFAULT_CAPACITY = 10

    def __init__(self):
        """Create an empty queue"""
        self.data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self.size = 0
        self.front = 0

    def __len__(self):
        """Return the number of elements in the queue."""
        return self.size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self.size == 0

    def first(self):
        """Return the element at the front of the queue.
        Raise Empty exception if the queue is empty"""
        if self.is_empty():
            raise Exception('Queue is empty')
        return self.data[self.front]

    def dequeue(self):
        """Remove and return the first element of the queue
        Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Exception('Queue is empty')
        answer = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % len(self.data)
        self.size -= 1
        return answer

    def enqueue(self, element):
        """ Add an element to the back of queue"""
        if self.size == len(self.data):
            self.resize(2*len(self.data))
        avail = (self.front + self.size) % len(self.data)
        self.data[avail] = element
        self.size += 1

    def resize(self, cap):
        """Resize to a new capacity >= len(self"""
        old = self.data
        self.data = [None] * cap
        walk = self.front
        for k in range(self.size):
            self.data[k] = old[walk]
            walk = (1 + walk) % len(old)
        self.front = 0




