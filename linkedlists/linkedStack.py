from .node import Node

class LinkedStack:
    """LIFO Stack implementation using a singly linked list for storage"""

    def __init__(self):
        """Create an empty stack"""
        self.head = None
        self.size = 0

    def __len__(self):
        """Return the number of elements in the stack"""
        return self.size

    def __repr__(self):
        """Return the whole stack with head in the start"""
        curr = self.head
        data = []
        while curr:
            data.append(str(curr.data))
            curr = curr.next
        return '\n|\n'.join(data)

    def is_empty(self):
        """Return True if the stack is empty"""
        return self.size == 0

    def push(self, data):
        """Add element to the top of the stack"""
        self.head = Node(data, self.head)
        self.size += 1

    def top(self):
        """Return the element at the top of the stack"""
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.head.data

    def pop(self):
        """Remove and return the element from the top of the stack"""
        if self.is_empty():
            raise Exception('Stack is empty')
        result = self.head.data
        self.head = self.head.next
        self.size -= 1
        return result