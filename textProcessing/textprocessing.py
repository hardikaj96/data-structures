
def find_brute(T, P):
    """Return the lowest index of T at which substring P begins """
    n, m = len(T), len(P)
    for i in range(n-m+1):
        k = 0
        while k < m and T[i+k] == P[k]:
            k += 1
        if k == m:
            return i
    return  -1

# find_brute("abacaabaccabacabaabb", "abacab")

def find_boyer_moore(T, P):
    """Return the lowest index of T at which substring P begins"""
    n, m = len(T), len(P)
    if m == 0:
        return 0
    last = {}
    for k in range(m):
        last[P[k]] = k
    i = m-1
    k = m-1
    while i < n:
        if T[i] == P[k]:
            if k == 0:
                return i
            else:
                i -= 1
                k -= 1
        else:
            j =  last.get(T[i], -1)
            i += m - min(k, j+1)
            k = m-1
    return -1

def find_kmp(T, P):
    """Return the lowest index of T at which substring P begins"""
    n, m = len(T), len(P)
    if m == 0:
        return 0
    fail = compute_kmp_fail(P)
    j = 0
    k = 0
    while j < n:
        if T[j] == P[k]:
            if k == m -1:
                return j - m + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k-1]
        else:
            j += 1
    return -1

def compute_kmp_fail(P):
    """Utility that computes and returns KMP 'fail' list"""
    m = len(P)
    fail = [0] * m
    j = 1
    k = 0
    while j < m:
        if P[j] == P[k]:
            fail[j] = k + 1
            j += 1
            k += 1
        elif k > 0:
            k = fail[k-1]
        else:
            j += 1

def matrix_chain(d):
    """d is a list of n+1 numbers such that size of kth matrix is d[k]-by-d[k+1]
    Return an n-by-n table such that N[i][j] represents the minimum number of
    multiplications needed to compute the product of Ai through Aj inclusive"""
    n = len(d) - 1
    N = [[0] * n for i in range(n)]
    for b in range(1, n):
        for i in range(n-b):
            j = i + b
            N[i][j] = min(N[i][k]+N[k+1][j]*d[i]*d[k+1]*d[j+1] for k in range(i,j))
    return N

def LCS(X, Y):
    """Return table such that L[j][k] is length of LCS for X[0:j] and Y[0:k]"""
    n, m =len(X), len(Y)
    L = [[0] *(m+1) for k in range(n+1)]
    for j in range(n):
        for k in range(m):
            if X[j] == Y[k]:
                L[j+1][k+1] = L[j][k] + 1
            else:
                L[j+1][k+1] = max(L[j][k+1], L[j+1][k])
    return L

def LCS_solution(X, Y, L):
    """Return the longest common substring of X and Y, given LCS table L"""
    solution = []
    j, k = len(X), len(Y)
    while L[j][k]>0:
        if X[j-1] == Y[k-1]:
            solution.append(X[j-1])
            j -= 1
            k -= 1
        elif L[j-1][k] >= L[j][k-1]:
            j -= 1
        else:
            k -= 1
    return ''.join(reversed(solution))