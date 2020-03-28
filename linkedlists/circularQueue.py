from .node import Node

class CircularQueue:
    """Queue implementation using circularly linked list for storage"""

    def __init__(self):
        """Create an empty queue"""
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
        head = self.tail.next
        return head.data

    def dequeue(self):
        """Remove and return the first element of the queue"""
        if self.is_empty():
            raise Exception('Queue is empty')
        oldhead = self.tail.next
        if self.size == 1:
            self.tail = None
        else:
            self.tail.next = oldhead.next
        self.size -= 1
        return oldhead.data

    def enqueue(self, data):
        """Add an element to the back of the queue"""
        new_node = Node(data)
        if self.is_empty():
            new_node.next = new_node
        else:
            new_node.next = self.tail.next
        self.tail = new_node
        self.size += 1

    def rotate(self):
        """Rotate front element to the back of queue"""
        if self.size > 0:
            self.tail = self.tail.next