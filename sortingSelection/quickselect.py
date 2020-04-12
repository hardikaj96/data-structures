import random

def quick_select(S, k):
    """Return the kth smallest element of list S, for k from 1 to len(S)"""
    if len(S) == 1:
        return S[0]
    pivot = random.choice(S)
    L = [x for x in S if x < pivot]
    E = [x for x in S if x == pivot]
    G = [x for x in S if pivot < x]
    if k <= len(L):
        return quick_select(L, k)
    elif k <= len(L) + len(E):
        return pivot
    else:
        j = k - len(L) - len(E)
        return quick_select(G, j)
