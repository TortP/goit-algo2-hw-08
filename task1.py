import random
import time
from collections import OrderedDict
from typing import List, Tuple


class LRUCache:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
            return
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)
        self.cache[key] = value

    def keys(self):
        return list(self.cache.keys())

    def invalidate_keys_containing_index(self, index: int):
        keys_to_remove = [k for k in self.cache.keys() if k[0] <= index <= k[1]]
        for k in keys_to_remove:
            del self.cache[k]

    def clear(self):
        self.cache.clear()


# Shared cache instance
_lru_cache = LRUCache(capacity=1000)


def range_sum_no_cache(array: List[int], left: int, right: int) -> int:
    return sum(array[left:right+1])


def update_no_cache(array: List[int], index: int, value: int) -> None:
    array[index] = value


def range_sum_with_cache(array: List[int], left: int, right: int) -> int:
    key = (left, right)
    cached = _lru_cache.get(key)
    if cached != -1:
        return cached
    res = sum(array[left:right+1])
    _lru_cache.put(key, res)
    return res


def update_with_cache(array: List[int], index: int, value: int) -> None:
    array[index] = value
    _lru_cache.invalidate_keys_containing_index(index)


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:        
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                                 
            if random.random() < p_hot:       
                left, right = random.choice(hot)
            else:                             
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries


def run_queries(array: List[int], queries: List[Tuple], use_cache: bool = False) -> float:
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            if use_cache:
                range_sum_with_cache(array, q[1], q[2])
            else:
                range_sum_no_cache(array, q[1], q[2])
        else:  # Update
            if use_cache:
                update_with_cache(array, q[1], q[2])
            else:
                update_no_cache(array, q[1], q[2])
    end = time.time()
    return end - start


def demo(n=100_000, q=50_000, seed=42, quick=True):
    random.seed(seed)
    array = [random.randint(1, 100) for _ in range(n)]
    queries = make_queries(n, q)

    arr1 = array.copy()
    arr2 = array.copy()

    _lru_cache.clear()
    t_no_cache = run_queries(arr1, queries, use_cache=False)

    _lru_cache.clear()
    t_with_cache = run_queries(arr2, queries, use_cache=True)

    speedup = t_no_cache / t_with_cache if t_with_cache > 0 else float('inf')

    print(f"Без кешу : {t_no_cache:.2f} c")
    print(f"LRU-кеш  : {t_with_cache:.2f} c  (прискорення ×{speedup:.2f})")


if __name__ == '__main__':
    demo(n=20000, q=5000)
