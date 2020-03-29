from .doublylinkedlist import DoublyLinkedList
class PositionalList(DoublyLinkedList):
    """A sequential container of elements allowing positional access"""

    class Position:
        """An abstraction representing the location of a single element"""

        def __init__(self, container, node):
            self.container = container
            self.node = node

        def element(self):
            """Return the element stored at this Position"""
            return self.node.element

        def __eq__(self, other):
            """Return True if other is a Position representing the same node"""
            return type(other) is type(self) and other.node is self.node

        def __ne__(self, other):
            """Return True if other does not represent the same location"""
            return not (self == other)

    def validate(self, p):
        """Return position's node, or raise appropriate error if invalid"""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('p does not belong to this container')
        if p.node.next is None:
            raise ValueError('p is no longer valid')
        return p.node

    def make_position(self, node):
        """Return Position instance for given node"""
        if node is self.header or node is self.trailer:
            return None
        else:
            return self.Position(self, node)

    def first(self):
        """Return the first Position in the list"""
        return self.make_position(self.header.next)

    def last(self):
        """Return the last Position in the list"""
        return self.make_position(self.trailer.prev)

    def before(self, p):
        """Return the Position just before Position p"""
        node = self.validate(p)
        return self.make_position(node.prev)

    def after(self, p):
        """Return the Position just after Position p"""
        node = self.validate(p)
        return self.make_position(node.next)

    def __iter__(self):
        """Generate a forward iteration of the elements of the list"""
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def insert_between(self, e, predecessor, successor):
        """Add element between existing nodes and return new Position"""
        node = super().insert_between(e, predecessor, successor)
        return self.make_position(node)

    def add_first(self, e):
        """Insert element e at the front of the list and return new Position"""
        return self.insert_between(e, self.header, self.header.next)

    def add_last(self, e):
        """Insert element e at the back of the list and return new Position"""
        return self.insert_between(e, self.trailer.prev, self.trailer)

    def add_before(self, p, e):
        """Insert element e into list before Position p and return new Position"""
        original = self.validate(p)
        return self.insert_between(e, original.prev, original)

    def add_after(self, p, e):
        """Insert element e into list after Position p and return new Position"""
        original = self.validate(p)
        return self.insert_between(e, original, original.next)

    def delete(self, p):
        """Remove and return the element at Position p"""
        original = self.validate(p)
        return self.delete_node(original)

    def replace(self, p, e):
        """Replace the element at Position p with e"""
        original = self.validate(p)
        old_value = original.element
        original.element = e
        return old_value

