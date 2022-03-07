#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Heap():
    def __init__(self, datas=None, identby=None, sortby=None, combmode="sum"): #id = identify by 
        self.cache = datas
        self.identby = identby
        self.sortby = sortby
        self.combmode = combmode
    
    def __len__(self):  #__bool__ :for bool method
        return self.hsize

    def __contains__(self, item):  #for in method
        return item in self.cache

    def idx(self, ident, identby=None):
        if identby is not None:
            self.identby =  identby
        if self.identby is None:
            return None
        for idx in range(self.hsize):
            if not hasattr(self.cache[idx], self.identby):
                return None
            _ident_attr = getattr(self.cache[idx], self.identby)
            if ident == _ident_attr:
                return idx + 1
        return None
    
    @property
    def identby(self):
        return self._identby

    @identby.setter
    def identby(self, identby):
        self._identby = identby
        
    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, datas):
        self._cache = []
        self._hsize = 0
        self._length = 0
        if isinstance(datas, list):
            for data in datas:
                self._cache.append(data)
                # print(str(self._cache[-1]))
            self._hsize = len(self._cache)
            self._length = len(self._cache)
        # print(self._cache)
        # raise Exception()

    @property
    def hsize(self):
        return self._hsize

    @hsize.setter
    def hsize(self, hsize):
        self._hsize = hsize

    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, length):
        self._length = length

    @property
    def sortby(self):
        return self._sortby

    @sortby.setter
    def sortby(self, sortby):
        self._sortby = sortby

    @property
    def combmode(self):
        return self._combmode

    @combmode.setter
    def combmode(self, mode):
        self._combmode = mode

    def parent(self, idx):
        return idx >> 1

    def left(self, idx):
        return idx << 1

    def right(self, idx):
        return (idx << 1) + 1

    def value(self, idx):
        if 1 <= idx <= self.length:
            if self.sortby:
                sortby = [self.sortby]
                if isinstance(self.sortby, list):
                    sortby = self.sortby
                if self.combmode == 'sum':
                    sum = 0
                    for by in sortby:
                        if hasattr(self.cache[idx-1], by):
                            sum += getattr(self.cache[idx-1], by)
                    return sum
            else:
                return self.cache[idx-1]
        else:            
            return None

    def item(self, idx):
        if 1 <= idx <= self.length:
            return self.cache[idx-1]
        else:
            return None
    
    def set_item(self, idx, value):
        if 1 <= idx <= self.length:
            self.cache[idx-1] = value

    def swap(self, first, second):
        self.cache[first-1], self.cache[second-1] = self.cache[second-1], self.cache[first-1]
    
    def min_heapify(self, idx):
        left = self.left(idx)
        right = self.right(idx)
        smallest = idx
        if left <= self.hsize and self.value(left) < self.value(idx):
            smallest = left
        if right <= self.hsize and self.value(right) < self.value(smallest):
            smallest = right
        if smallest != idx:
            self.swap(smallest, idx)
            self.min_heapify(smallest)

    def build_min_heap(self):
        # print(self.cache)
        bgn = self.hsize >> 1
        for i in range(bgn, 0, -1):
            # print("build: {}".format(i))
            self.min_heapify(i)


class PriorityQueue(Heap):
    def __init__(self, datas=None, identby=None, sortby=None):
        # print(datas, type(datas))
        super().__init__(datas=datas, identby=identby, sortby=sortby)
        self.build_min_heap()
    
    @property
    def head(self):
        return self.item(1)

    @property
    def tail(self):
        return self.item(self.hsize)

    def enqueue(self, value):
        return self.insert(value)

    def dequeue(self):
        return self._extract_minimum()

    def resort(self, sortby=None):
        if sortby:
            self.sortby = sortby
        self.build_min_heap()

    def minimum(self):
        return self.item(1)

    def _extract_minimum(self):
        minimum = self.item(1)
        # print("minimum: ", minimum.__dict__)
        # print("_extract_minimum, hsize", self.hsize, self.item(self.hsize))
        self.set_item(1, self.item(self.hsize))
        self.hsize -= 1
        self.min_heapify(1)
        # print("heap size: {}".format(self.hsize))
        return minimum

    def insert(self, value):
        if self.hsize < self.length:
            self.cache[self.hsize] = value
            self.hsize += 1
        else:
            self.cache.append(value)
            self.hsize += 1
            self.length += 1
        # print("heap size: {}".format(self.hsize))
        self._decrease_idx(self.hsize)
    
    def delete(self, ident, identby=None): #begin from 1
        _idx = self.idx(ident, identby)
        if not _idx: #not None
            return False
        self.swap(self.hsize, _idx)
        self.hsize -= 1
        self.min_heapify(_idx)
        return True

    def _decrease_idx(self, idx):
        while idx > 0:
            if self.parent(idx) and self.value(self.parent(idx)) > self.value(idx):
                self.swap(self.parent(idx), idx)
            idx = self.parent(idx)


if __name__ == "__main__":
	pass
