from trees import tree

def test_trees():
    T = tree.Tree()
    root = T.add_root(5)
    left = T.add_left(root, 6)
    right = T.add_right(root, 7)
    print(list(T.preorder_traversal(root)))

test_trees()