class EulerTour:
    """Abstract base class for performing Euler tour of a tree"""
    def __init__(self, tree):
        """Prepare an Euler tour template for given tree"""
        self._tree = tree

    def tree(self):
        """Return reference to the tree being traversed"""
        return self._tree

    def execute(self):
        """Perform the tour and return any result from post visit of root"""
        if len(self._tree) > 0:
            return self.tour(self._tree.root(), 0, [])

    def tour(self, p, d, path):
        """Perform tour of subtree rooted at Position p

        p       Position of current node being visited
        d       depth of p in the tree
        path    list of indices of children on path from root to p"""
        self.hook_previsit(p, d, path)
        results = []
        path.append(0)
        for c in self._tree.children(p):
            results.append(self.tour(c, d+1, path))
            path[-1] += 1
        path.pop()
        answer = self.hook_postvisit(p, d, path, results)
        return answer

    def hook_previsit(self, p, d, path):
        pass

    def hook_postvisit(self, p, d, path, results):
        pass

class PreorderPrintIndentedTour(EulerTour):
    def hook_previsit(self, p, d, path):
        print(2*d*' ' + str(p.element()))

class PreorderPrintIndentedLabeledTour(EulerTour):
    def hook_previsit(self, p, d, path):
        label = '.'.join(str(j+1) for j in path)
        print(2*d*' ' + label, p.element())

class ParenthesizeTour(EulerTour):
    def hook_previsit(self, p, d, path):
        if path and path[-1]>0:
            print(', ',end='')
        print(p.element(), end='')
        if not self.tree().is_leaf(p):
            print(' (', end='')

    def hook_postvisit(self, p, d, path, results):
        if not self.tree().is_leaf(p):
            print(') ', end='')

class DiskSpaceTour(EulerTour):
    def hook_postvisit(self, p, d, path, results):
        return p.element().space()+sum(results)

class BinaryEulerTour(EulerTour):
    """Abstract base class for performing Euler tour of a binary tree"""
    def tour(self, p, d, path):
        results = [None, None]
        self.hook_previsit(p, d, path)
        if self._tree.left(p) is not None:
            path.append(0)
            results[0] = self.tour(self._tree.left(p), d+1, path)
            path.pop()
        self.hook_invisit(p, d, path)
        if self._tree.right(p) is not None:
            path.append(1)
            results[1] = self.tour(self._tree.right(p), d+1, path)
            path.pop()
        answer = self.hook_postvisit(p, d, path, results)
        return answer

    def hook_invisit(self, p, d, path):
        pass

class BinaryLayout(BinaryEulerTour):
    """Class for computing (x,y) coordinates for each node of a binary tree"""
    def __init__(self, tree):
        super().__init__(tree)
        self.count = 0

    def hook_invisit(self, p, d, path):
        p.element().setX(self.count)
        p.element().setY(d)
        self.count += 1