from trees.tree import Tree
from hashTables.maps import MapBase

class TreeMap(Tree, MapBase):
    """Sorted Map implementing using a binary search tree"""

    class Position(Tree.Position):
        def key(self):
            """Return key of map's key-value pair"""
            return self.element().key

        def value(self):
            """Return value of map's key-value pair"""
            return self.element().value

    def subtree_search(self, p, k):
        """Return Position of p's subtree having k, or last node searched"""
        if k == p.key():
            return p
        elif k < p.key():
            if self.left(p) is not None:
                return self.subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                return self.subtree_search(self.right(p), k)
        return p

    def subtree_first_position(self, p):
        """Return Position of first item in subtree rooted at p"""
        walk = p
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk

    def subtree_last_position(self, p):
        """Return Position of last item in subtree rooted at p"""
        walk = p
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    def first(self):
        """Return the first Position in the tree"""
        return self.subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        """Return the last Position in the tree"""
        return self.subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, p):
        """Return the Position just before p in the natural order
        Return None if p is the first Position"""

        self.validate(p)
        if self.left(p):
            return self.subtree_last_position(self.left(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        """Return teh Position just after p in the natural order"""
        self.validate(p)
        if self.right(p):
            return self.subtree_first_position(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        """Return position with k, or else neighbor"""
        if self.is_empty():
            return None
        else:
            p = self.subtree_search(self.root(), k)
            self.rebalance_access(p)
            return p

    def find_min(self):
        """Return (key,value) pair with minimum key"""
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_ge(self, k):
        """Return (key,value) pair with least key greater than or equal to k"""
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if p.key()<k:
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop
        if start is None, iteration begins with minimum key of map.
        if stop is None, iteration continues through the maximum key of map"""
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

    def __getitem__(self, k):
        """Return value associated with key k"""
        if self.is_empty():
            raise KeyError('Key Error: ' + repr(k))
        else:
            p = self.subtree_search(self.root1(), k)
            self.rebalance_access(p)
            if k != p.key():
                raise KeyError('Key Error: ' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present"""
        if self.is_empty():
            leaf = self.add_root(self.Item(k, v))
        else:
            p = self.subtree_search(self.root1(), k)
            if p.key() == k:
                p.element().value = v
                self.rebalance_access(p)
                return
            else:
                item = self.Item(k, v)
                if p.key() < k:
                    leaf = self.add_right(p, item)
                else:
                    leaf = self.add_left(p, item)
        self.rebalance_insert(leaf)

    def __iter__(self):
        """Generate an iteration of all keys in the map in order"""
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def delete(self, p):
        """Remove the item at given Position"""
        self.validate(p)
        if self.left(p) and self.right(p):
            replacement = self.subtree_last_position(self.left(p))
            self.replace(p, replacement.element())
            p = replacement
        parent = self.parent(p)
        self.delete(p)
        self.rebalance_delete(parent)

    def __delitem__(self, k):
        """Remove item associated with key k"""
        if not self.is_empty():
            p = self.subtree_search(self.root1(), k)
            if k == p.key():
                self.delete(p)
                return
            self.rebalance_access(p)
        raise KeyError('Key Error: ' + repr(k))

    def relink(self, parent, child, make_left_child):
        """Relink parent node with child node"""
        if make_left_child:
            parent.left = child
        else:
            parent.right = child
        if child is not None:
            child.parent = parent

    def rotate(self, p):
        """Rotate Position p above its parent"""
        x = p.node
        y = x.parent
        z = y.parent
        if z is None:
            self.root = x
            x.parent = None
        else:
            self.relink(z, x, y == z.left)
        if x == y.left:
            self.relink(y, x.right, True)
            self.relink(x, y, False)
        else:
            self.relink(y, x.left, False)
            self.relink(x, y, True)

    def restructure(self, x):
        """Perform trinode restructure of Position x with parent/grandparent"""
        y = self.parent(x)
        z = self.parent(y)
        if (x == self.right(y)) == (y == self.right(z)):
            self.rotate(y)
            return y
        else:
            self.rotate(x)
            self.rotate(x)
            return x

class AVLTreeMap(TreeMap):
    """Sorted map implementation using an AVL tree"""

    class Node(TreeMap.Node):
        """Node class for AVL maintains height value for balancing"""

        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self.height = 0

        def left_height(self):
            return self.left.height if self.left is not None else 0

        def right_height(self):
            return self.right.height if self.right is not None else 0

    def recompute_height(self, p):
        p.node.height = 1 + max(p.node.left_height(), p.node.right_height())

    def is_balanced(self, p):
        return abs(p.node.left_height() - p.node.right_height()) <= 1

    def tall_child(self, p, favorleft=False):
        if p.node.left_height() + (1 if favorleft else 0) > p.node.right_height():
            return self.left(p)
        else:
            return self.right(p)

    def tall_grandchild(self, p):
        child = self.tall_child(p)
        alignment = (child == self.left(p))
        return self.tall_child(child, alignment)

    def rebalance(self, p):
        while p is not None:
            old_height = p.node.height
            if not self.is_balanced(p):
                p = self.restructure(self.tall_grandchild(p))
                self.recompute_height(self.left(p))
                self.recompute_height(self.right(p))
            self.recompute_height(p)
            if p.node.height == old_height:
                p = None
            else:
                p = self.parent(p)

    def rebalance_insert(self, p):
        self.rebalance(p)

    def rebalance_delete(self, p):
        self.rebalance(p)

class SplayTreeMap(TreeMap):
    """Sorted map implementation using a splay tree"""

    def splay(self, p):
        while p != self.root1():
            parent = self.parent(p)
            grand = self.parent(parent)
            if grand is None:
                self.rotate(p)
            elif (parent == self.left(grand)) == (p == self.left(parent)):
                self.rotate(parent)
                self.rotate(p)
            else:
                self.rotate(p)
                self.rotate(p)

    def rebalance_insert(self, p):
        self.splay(p)

    def rebalance_delete(self, p):
        if p is not None:
            self.splay(p)

    def rebalance_access(self, p):
        self.splay(p)

class RedBlackTreeMap(TreeMap):
    """Sorted map implementation using a red-black tree"""

    class Node(TreeMap.Node):
        """Node class for red-black tree maintains bit that denotes color"""
        __slots__ = 'red'

        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self.red = True

    def set_red(self, p):
        p.node.red = True

    def set_black(self, p):
        p.node.red = False

    def set_color(self, p, make_red):
        p.node.red = make_red

    def is_red(self, p):
        return p is not None and p.node.red

    def is_red_leaf(self, p):
        return self.is_red(p) and self.is_leaf(p)

    def get_red_child(self, p):
        """Return a red child of p"""
        for child in (self.left(p), self.right(p)):
            if self.is_red(child):
                return child
            return None

    def rebalance_insert(self, p):
        self.resolve_red(p)


    def resolve_red(self, p):
        if self.is_root(p):
            self.set_black(p)
        else:
            parent = self.parent(p)
            if self.is_red(parent):
                uncle = self.sibling(parent)
                if not self.is_red(uncle):
                    middle = self.restructure(p)
                    self.set_black(middle)
                    self.set_red(self.left(middle))
                    self.set_red(self.right(middle))
                else:
                    grand = self.parent(parent)
                    self.set_red(grand)
                    self.set_black(self.left(grand))
                    self.set_black(self.right(grand))
                    self.resolve_red(grand)

    def rebalance_delete(self, p):
        if len(self) == 1:
            self.set_black(self.root1())
        elif p is not None:
            n = self.num_children(p)
            if n == 1:
                c = next(self.children(p))
                if not self.is_red_leaf(c):
                    self.fix_deficit(p, c)
            elif n == 2:
                if self.is_red_leaf(self.left(p)):
                    self.set_black(self.left(p))
                else:
                    self.set_black(self.right(p))

    def fix_deficit(self, z, y):
        """Resolve black deficit at z, where y is the root of z's heavier subtree"""
        if not self.is_red(y):
            x = self.get_red_child(y)
            if x is not None:
                old_color = self.is_red(z)
                middle = self.restructure(x)
                self.set_color(middle, old_color)
                self.set_black(self.left(middle))
                self.set_black(self.right(middle))
            else:
                self.set_red(y)
                if self.is_red(z):
                    self.set_black(z)
                elif not self.is_root(z):
                    self.fix_deficit(self.parent(z), self.sibling(z))
        else:
            self.rotate(y)
            self.set_black(y)
            self.set_red(z)
            if z == self.right(y):
                self.fix_deficit(z, self.left(z))
            else:
                self.fix_deficit(z, self.right(z))
