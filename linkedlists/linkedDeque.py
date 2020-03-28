from .doublylinkedlist import DoublyLinkedList

class LinkedDeque(DoublyLinkedList):
    """Double ended queue implementation"""

    def first(self):
        """Return the element at the front of the queue"""
        if self.is_empty():
            raise Exception('Deque is empty')
        return self.header.next.element

    def last(self):
        """Return the element at the back of the deque"""
        if self.is_empty():
            raise Exception('Deque is empty')
        return self.trailer.prev.element

    def insert_first(self, data):
        """Add an element to the front of the deque"""
        self.insert_between(data, self.header, self.header.next)

    def insert_last(self, data):
        """Add an element to the back of the deque"""
        self.insert_between(data, self.trailer.prev, self.trailer)

    def delete_first(self):
        """Remove and return the element from the front of the deque"""
        if self.is_empty():
            raise Exception('Deque is empty')
        return self.delete_node(self.header.next)

    def delete_last(self):
        """Remove and return the element from the back of the deque"""
        if self.is_empty():
            raise Exception('Deque is empty')
        return self.delete_node(self.trailer.prev)

