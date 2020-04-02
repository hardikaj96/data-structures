from trees import tree

def test_trees():
    T = tree.Tree()
    root = T.add_root(5)
    left = T.add_left(root, 6)
    right = T.add_right(root, 7)
    leftl = T.add_left(left, 2)
    leftr = T.add_right(left, 3)
    rightl = T.add_left(right, 8)
    rightr = T.add_right(right, 9)
    print(list(T.preorder()))
    print(list(T.postorder()))
    print(list(T.inorder()))
    print(list(T.breadthfirst()))
test_trees()

def build_expression_tree(tokens):
    """Returns an Expression Tree based upon by a tokenized expression"""
    S = []
    for t in tokens:
        if t in '+-x*/':
            S.append(t)
        elif t not in '()':
            S.append(tree.ExpressionTree(t))
        elif t == ')':
            right = S.pop()
            op = S.pop()
            left = S.pop()
            S.append(tree.ExpressionTree(op, left, right))
    return S.pop()