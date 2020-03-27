from .node import Node

class LinkedQueue:
    """FIFO queue implementation using a singly linked list"""

    def __init__(self):
        """Create an empty queue"""
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """Return the number of elements in the queue"""
        return self.size

    def is_empty(self):
        """Return True if the queue is empty"""
        return self.size == 0

    def first(self):
        """Return the element at the front of the queue"""
        if self.is_empty():
            raise Exception('Queue is empty')
        return self.head.data

    def dequeue(self):
        """Remove and return the first element of the queue"""
        if self.is_empty():
            raise Exception('Queue is empty')
        result = self.head.data
        self.head = self.head.next
        self.size -= 1
        if self.is_empty():
            self.tail = None
        return result

    def enqueue(self, data):
        """Add an element to the back of queue"""
        node = Node(data)
        if self.is_empty():
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.size += 1
