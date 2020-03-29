class Node:
    def __init__(self, element, prev, next):
        """Initialize node's fields"""
        self.element = element
        self.prev = prev
        self.next = next

class DoublyLinkedList:
    """A base class for doubly Linked list representation"""

    def __init__(self):
        """Create an empty list"""

        self.header = Node(None, None, None)
        self.trailer = Node(None, None, None)
        self.header.next = self.trailer
        self.trailer.prev = self.header
        self.size = 0

    def __len__(self):
        """Return the number of elements in the list"""
        return self.size

    def is_empty(self):
        """Return True if the list is empty"""
        return self.size == 0

    def insert_between(self, element, predecessor, successor):
        """Add data between two existing nodes and return new node"""
        new_node = Node(element, predecessor, successor)
        predecessor.next = new_node
        successor.prev = new_node
        self.size += 1
        return new_node

    def delete_node(self, node):
        """Delete node from the list and return its data"""
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1
        data = node.element
        node.prev = node.next = node.element = None
        return data