from math import log
from scal2.utils import s_join

from heapq import heappush

class MaxHeap(list):
    def copy(self):
        return MaxHeap(self[:])
    def exch(self, i, j):
        self[i], self[j] = self[j], self[i]
    less = lambda self, i, j: self[i][0] > self[j][0]
    def swim(self, k):
        while k > 0:
            j = (k-1) // 2
            if self.less(k, j):
                break
            self.exch(k, j)
            k = j
    def sink(self, k):
        N = len(self)
        while True:
            j = 2*k + 1
            if j > N-1:
                break
            if j < N-1 and self.less(j, j+1):
                j += 1
            if self.less(j, k):
                break
            self.exch(k, j)
            k = j
    add = lambda self, key, value: heappush(self, (-key, value))
    moreThan = lambda self, key: self.moreThanStep(key, 0)
    def moreThanStep(self, key, index):
        if index < 0:
            return []
        try:
            item = self[index]
        except IndexError:
            return []
        if -item[0] <= key:
            return []
        return [
                (-item[0], item[1])
            ] + \
            self.moreThanStep(key, 2*index+1) + \
            self.moreThanStep(key, 2*index+2)
    __str__ = lambda self: ' '.join(['%s'%(-k) for k, v in self])
    def delete(self, key, value):
        try:
            index = self.index((-key, value))## not optimal FIXME
        except ValueError:
            pass
        else:
            self.deleteIndex(index)
    def deleteIndex(self, index):
        N = len(self)
        if index < 0 or index > N-1:
            raise ValueError('invalid index to deleteIndex()')
        if index == N-1:
            return self.pop(index)
        self.exch(index, N-1)
        key = -self.pop(N-1)[0]
        self.sink(index)
        self.swim(index)
        return key
    verify = lambda self: self.verifyIndex(0)
    def verifyIndex(self, i):
        assert i >= 0
        try:
            k = self[i]
        except IndexError:
            return True
        try:
            if self[2*i + 1] < k:
                print '[%s] > [%s]'%(2*i + 1, i)
                return False
        except IndexError:
            return True
        try:
            if self[2*i + 2] < k:
                print '[%s] > [%s]'%(2*i + 2, i)
                return False
        except IndexError:
            return True
        return self.verifyIndex(2*i + 1) and self.verifyIndex(2*i + 2)
    getAll = lambda self: [(-key, value) for key, value in self]
    def getMax(self):
        if not self:
            raise ValueError('heap empty')
        k, v = self[0]
        return -k, v
    def getMin(self):
        ## at least 2 times faster than max(self)
        if not self:
            raise ValueError('heap empty')
        k, v = max(
            self[-2**int(
                log(len(self), 2)
            ):]
        )
        return -k, v
    '''
    def deleteLessThanStep(self, key, index):
        try:
            key1, value1 = self[index]
        except IndexError:
            return
        key1 = -key1
        #if key
    def deleteLessThan(self, key):
        pass
    '''


def getMinTest(N):
    from random import randint
    from time import time
    h = MaxHeap()
    for i in range(N):
        x = randint(1, 10*N)
        h.add(x, 0)
    t0 = time()
    k1 = -max(h)[0]
    t1 = time()
    k2 = h.getMin()[0]
    t2 = time()
    assert k1 == k2
    #print 'time getMin(h)/min(h) = %.5f'%((t2-t1)/(t1-t0))
    #print 'min key = %s'%k1

def testDeleteStep(N, maxKey):
    from random import randint
    from heapq import heapify
    ###
    h = MaxHeap()
    for i in range(N):
        h.add(randint(0, maxKey), 0)
    h0 = h.copy()
    rmIndex = randint(0, N-1)
    rmKey = -h[rmIndex][0]
    rmKey2 = h.deleteIndex(rmIndex)
    if not h.verify():
        print 'not verified, N=%s, I=%s'%(N, rmIndex)
        print h0
        print h
        print '------------------------'
        return False
    return True


def testDelete():
    for N in range(10, 30):
        for p in range(10000):
            if not testDeleteStep(N, 10000):
                break

#if __name__=='__main__':
#    testDelete()




