class ArrayStack:
    """LIFO Stack implementation using a Python list as underlying storage"""

    def __init__(self):
        """Create an empty stack."""
        self.data = []

    def __len__(self):
        """Return the number of elements in the stack"""
        return len(self.data)

    def is_empty(self):
        """Return True is the stack is empty"""
        return len(self.data) == 0

    def push(self, element):
        """Add element to the top of the stack"""
        self.data.append(element)

    def top(self):
        """Return the element at the top of the stack
        Raise Empty exception if the stack is empty"""
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.data[-1]

    def pop(self):
        """Remove and return the element from the top of the stack
        Raise Empty excepton if the stack is empty"""
        if self.is_empty():
            raise Exception('Stack is empty')
        return self.data.pop()
