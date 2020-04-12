
from linkedlists.linkedQueue import LinkedQueue
import math

class MergeSort1:
    def merge(self, S1, S2, S):
        """Merge two sorted Python lists S1 and S2 into properly sized list S"""
        i = j =0
        while i + j <len(S):
            if i == len(S2) or (i < len(S1) and S1[i] < S2[j]):
                S[i+j] = S1[i]
                i += 1
            else:
                S[i+j] = S1[i]
                j += 1

    def merge_sort(self, S):
        """Sort the elements of Python list S using the merge-sort algorithm"""
        n = len(S)
        if n < 2:
            return
        mid = n // 2
        S1 = S[0:mid]
        S2 = S[mid:n]

        self.merge_sort(S1)
        self.merge_sort(S2)
        self.merge(S1, S2, S)

class MergeSort2:
    def merge(self, S1, S2, S):
        """Merge two sorted queue instances S1 and S2 into empty queu S"""
        while not S1.is_empty() and not S2.is_empty():
            if S1.first() < S2.first():
                S.enqueue(S1.dequeue())
            else:
                S.enqueue(S2.dequeue())
        while not S1.is_empty():
            S.enqueue(S1.dequeue())
        while not S2.is_empty():
            S.enqueue(S2.dequeue())

    def merge_sort(self, S):
        """Sort the elements of queue S using the merge-sort algorithm"""
        n = len(S)
        if n<2:
            return
        S1 = LinkedQueue()
        S2 = LinkedQueue()
        while len(S1) < n // 2:
            S1.enqueue(S.dequeue())
        while not S.is_empty():
            S2.enqueue(S.dequeue())
        self.merge_sort(S1)
        self.merge_sort(S2)
        self.merge(S1, S2, S)

class MergeSort3:
    def merge(self, src, result, start, inc):
        """Merge src[start:start+inc] and src[start+inc:start+2*inc] into result"""
        end1 = start+inc
        end2 = min(start+2*inc, len(src))
        x, y, z = start, start+inc, start
        while x < end1 and y < end2:
            if src[x] < src[y]:
                result[z] = src[x]
                x += 1
            else:
                result[z] = src[y]
                y += 1
        if x < end1:
            result[z:end2] = src[x:end1]
        elif y < end2:
            result[z:end2] = src[y:end2]

    def merge_sort(self, S):
        """Sort the elements of Python list S using the merge-sort algorithm"""
        n = len(S)
        logn = math.ceil(math.log(n, 2))
        src, dest = S, [None] * n
        for i in (2**k for k in range(logn)):
            for j in range(0, n, 2*i):
                self.merge(src, dest, j, i)
            src, dest = dest, src
        if S is not src:
            S[0:n] = src[0:n]
