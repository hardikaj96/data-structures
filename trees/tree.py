class Tree:
    """Abstract base class representing a tree structure"""

    class Node:

        def __init__(self, element, parent=None, left=None, right=None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right

    class Position:
        """An abstraction representing the location of a single element"""

        def __init__(self, container, node):
            """Constructor should not be invoked by user"""
            self.container = container
            self.node = node

        def element(self):
            """Return the element stored at this Position"""
            return self.node.element

        def __eq__(self, other):
            """Return True if other is a Position representing the same location"""
            return type(other) is type(self) and other.node is self.node

    def validate(self, p):
        """Return associated node if position is valid"""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p.container is not self:
            raise ValueError('p does not belong to this container')
        if p.node.parent is p.node:
            raise ValueError('p is no longer valid')
        return p.node

    def make_position(self, node):
        """Return Position instance for given node"""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        """Create an initially empty binary tree"""
        self.root = None
        self.size = 0

    def __len__(self):
        """Return the total number of elements in the tree"""
        return self.size

    def root(self):
        """Return the root Position of the tree"""
        return self.make_position((self.root))

    def parent(self, p):
        """Return the Position of p's parent"""
        node = self.validate(p)
        return self.make_position(node.parent)

    def left(self, p):
        """Return the Position of p's left child"""
        node = self.validate(p)
        return self.make_position(node.left)

    def right(self, p):
        """Return the Position of p's right child"""
        node = self.validate(p)
        return self.make_position(node.right)

    def is_root(self, p):
        """Return True if Position p represents the root of the tree"""
        return self.root() == p

    def is_leaf(self, p):
        """Return True if Position p does not have any children"""
        return self.num_children(p) == 0

    def is_empty(self):
        """Return True if the tree is empty"""
        return len(self) == 0

    def depth(self, p):
        """Return the number of levels separating Position p from the root"""
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def height1(self):
        """Return the height of the tree"""
        return max(self.depth(p) for p in self.positions() if self.is_lead(p))

    def height2(self, p):
        """Return the height of the subtree rooted at Position p"""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self.height2(c) for c in self.children(p))

    def height(self, p=None):
        """Return the height of the subtree rooted at Position p
        if p is None, return the height of the entire tree"""
        if p is None:
            p = self.root()
        return self.height2(p)

    def sibling(self, p):
        """Return a Position representating p's sibling """
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        """Generate an iteration of Positions representing p's children"""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def num_children(self, p):
        """Return the number of children of Position p"""
        node = self.validate(p)
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    def add_root(self, e):
        """Place element e at the root of an empty Tree and return new Position"""
        if self.root is not None:
            raise ValueError('Root exists')
        self.size = 1
        self.root = self.Node(e)
        return self.make_position(self.root)

    def add_left(self, p, e):
        """Create a new left child for Position p, storing element e
        Return the Position of new node"""
        node = self.validate(p)
        if node.left is not None:
            raise ValueError('Left child exists')
        self.size += 1
        node.left = self.Node(e, node)
        return self.make_position(node.left)

    def add_right(self, p, e):
        """Create a new right child for Position p, storing element e
        Return the Position of new node"""
        node = self.validate(p)
        if node.right is not None:
            raise ValueError('Right child exists')
        self.size += 1
        node.right = self.Node(e, node)
        return self.make_position(node.right)

    def replace(self, p, e):
        """Replace the element at position p with e, and return old element"""
        node = self.validate(p)
        old = node.element
        node.element = e
        return old

    def delete(self, p):
        """Delete the node at Position p, and replace it with its child
        Return the element that had been stored at Position p"""
        node = self.validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children')
        child = node.left if node.left else node.right
        if child is not None:
            child.parent = node.parent
        if node is self.root:
            self.root = child
        else:
            parent = node.parent
            if node is parent.left:
                parent.left = child
            else:
                parent.right = child
        self.size -= 1
        node.parent = node
        return node.element

    def attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p"""
        node = self.validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match')
        self.size += len(t1) + len(t2)
        if not t1.is_empty():
            t1.root.parent = node
            t1.root = None
            t1.size = 0
        if not t2.is_empty():
            t2.root.parent = node
            t2.root = None
            t2.size = 0

    def preorder_traversal(self, p):
        """Preorder Traversal of the tree p"""
        if p is not None:
            yield p.element()
            for each_child in self.children(p):
                self.preorder_traversal(each_child)