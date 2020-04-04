from _collections import MutableMapping
from random import randrange

class MapBase(MutableMapping):
    """Our own abstract base class that includes a nonpublic Item class"""

    class Item:
        """Lightweight composite to store key-value pairs as map items"""

        def __init__(self, k, v):
            self.key = k
            self.value = v

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self.key < other.key

class UnsortedTableMap(MapBase):
    """Map implementation using an unordered list"""

    def __init__(self):
        """Create an empty map"""
        self.table = []

    def __getitem__(self, k):
        """Return value associated with key k"""
        for item in self.table:
            if k == item.key:
                return item.value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, key, value):
        """Assign value to key overwriting existing value if present"""
        for item in self.table:
            if key == item.key:
                item.value = value
                return
        self.table.append(self.Item(key, value))

    def __delitem__(self, k):
        """Remove item associated with key k"""
        for j in range(len(self.table)):
            if k == self.table[j].key:
                self.table.pop(j)
                return
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        """Return number of items in the map"""
        return len(self.table)

    def __iter__(self):
        """Generate iteration of the map's keys"""
        for item in self.table:
            yield item.key

class HashMapBase(MapBase):
    """Abstract base class for map using hash-table with MAD compression"""
    def __init__(self, cap=11, p=109345121):
        """Create an empty hash-table map"""
        self.table = cap * [None]
        self.n = 0
        self.prime = p
        self.scale = 1 + randrange(p-1)
        self.shift = randrange(p)

    def hash_function(self, k):
        return (hash(k)*self.scale + self.shift) % self.prime % len(self.table)

    def __len__(self):
        return self.n

    def __getitem__(self, k):
        j = self.hash_function(k)
        return self.bucket_getitem(j, k)

    def __setitem__(self, k, v):
        j = self.hash_function(k)
        self.bucket_setitem(j, k, v)
        if self.n > len(self.table) // 2:
            self.resize(2*len(self.table)-1)

    def __delitem__(self, k):
        j = self.hash_function(k)
        self.bucket_delitem(j, k)
        self.n -= 1

    def resize(self, c):
        old = list(self.items())
        self.table = c * [None]
        self.n = 0
        for (k,v) in old:
            self[k] = v

class ChainHashMap(HashMapBase):
    """Hash map implemented with separate chaining for collision resolution"""

    def bucket_getitem(self, j, k):
        bucket = self.table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        return bucket[k]

    def bucket_setitem(self, j, k, v):
        if self.table[j] is None:
            self.table[j] = UnsortedTableMap()
        oldsize = len(self.table[j])
        self.table[j][k] = v
        if len(self.table[j] > oldsize):
            self.n += 1

    def bucket_delitem(self, j, k):
        bucket = self.table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(k))
        def bucket[k]

    def __iter__(self):
        for bucket in self.table:
            if bucket is not None:
                for key in bucket:
                    yield key


class ProbeHashMap(HashMapBase):
    """Hash map implemented with linear probing for collision resolution"""
    AVAIL = object()

    def is_available(self, j):
        """Return True if index j is available in table"""
        return self.table[j] is None or self.table[j] is ProbeHashMap.AVAIL

    def find_slot(self, j, k):
        """Search for key k in bucket at index j

        Return (success, index) tuple described as follows
        if match was found, success is True and index denotes its location
        if no match found, success is False and index denotes first available slot"""
        firstAvail = None
        while True:
            if self.is_available(j):
                if firstAvail is None:
                    firstAvail = j
                if self.table[j] is None:
                    return (True, j)
            j = (j + 1) % len(self.table)

    def bucket_getitem(self, j, k):
        found, s = self.find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        return self.table[s].value

    def bucket_setitem(self, j, k, v):
        found, s = self.find_slot(j, k)
        if not found:
            raise KeyError('Key Error: ' + repr(k))
        self.table[s] = ProbeHashMap.AVAIL

    def __iter__(self):
        for j in range(len(self.table)):
            if not self.is_available(j):
                yield self.table[j].key

class SortedTableMap(MapBase):
    """Map implementation using a sorted table"""

    def find_index(self, k, low, high):
        """Return index of the leftmost item with key greater than or equal to k
        Return high + 1 if no such item qualifies
        That is, j will be returned such that:
            all items of slice table[low:j] have key < k
            all items of slice table[j:high+1] have key >= k
        """
        if high < low:
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self.table[mid].key:
                return mid
            elif k < self.table[mid].key:
                return self.find_index(k, low, mid-1)
            else:
                return self.find_index(k, mid+1, high)

    def __init__(self):
        """Create an empty map"""
        self.table = []

    def __len__(self):
        """Return number of items in the map"""
        return len(self.table)

    def __getitem__(self, k):
        """Return value associated with key k"""
        j = self.find_index(k, 0, len(self.table)-1)
        if j == len(self.table) or self.table[j].key != k:
            raise KeyError('Key Error: ' + repr(k))
        return self.table[j].value

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present"""
        j = self.find_index(k, 0, len(self.table)-1)
        if j < len(self.table) and self.table[j].key == k:
            self.table[j].value = v
        else:
            self.table.insert(j, self.Item(k,v))

    def __delitem__(self, k):
        """Remove item associated with k"""
        j = self.find_index((k, 0, len(self.table)-1))
        if j == len(self.table) or self.table[j].key != k:
            raise KeyError('Key Error: '+repr(k))
        self.table.pop()

    def __iter__(self):
        """Generate keys of the map ordered from minimum to maximum"""
        for item in self.table:
            yield item.key

    def find_min(self):
        """Return (key, value) pair with maximum key (or None if empty)"""
        if len(self.table) > 0:
            return (self.table[-1].key, self.table[-1].value)
        else:
            return None

    def find_ge(self, k):
        """Return (key, value) pair with least key greater than or equal to k."""
        j = self.find_index(k, 0, len(self.table)-1)
        if j < len(self.table):
            return (self.table[j].key, self.table[j].value)
        else:
            return None

    def find_lt(self, k):
        """Return (key, value) pair with greatest key strictly less than k"""
        j = self.find_index(k, 0, len(self.table)-1)
        if j > 0:
            return (self.table[j-1].key, self.table[j-1].value)
        else:
            return None

    def find_gt(self, k):
        """Return (key, value) pair with least key strictly greater than k"""
        j = self.find_index(k, 0, len(self.table)-1)
        if j < len(self.table) and self.table[j].key == k:
            j += 1
        if j < len(self.table):
            return (self.table[j].key, self.table[j].value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (key, value) pairs such that start <= key < stop

        If start is None, iteration begins with minimum key of map
        If stop is None, iteration continues through the maximum key of map
        """
        if start is None:
            j = 0
        else:
            j = self.find_index(start, 0, len(self.table)-1)
        while j < len(self.table) and (stop is None or self.table[j].key < stop):
            yield (self.table[j].key, self.table[j].value)
            j += 1

class CostPerformanceDatabase:
    """Maintain a database of maximal (cost, performance) pairs"""

    def __init__(self):
        """Create an empty database"""
        self.M = SortedTableMap()

    def best(self, c):
        """Return (cost, performance) pair with largest cost not exceeding c"""
        return self.M.find_le(c)

    def add(self, c, p):
        """Add new entry with cost c and performance p"""
        other = self.M.find_le(c)
        if other is not None and other[1] >= p:
            return
        self.M[c] = p
        other = self.M.find_gt(c)
        while other is not None and other[1] <= p:
            del self.M[other[0]]
            other = self.M.find_gt(c)
