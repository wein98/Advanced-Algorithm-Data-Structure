# Chia Wei Ying
# 30113199

import math

class FibonacciHeap:
    def __init__(self):
        self.rootHead, self.min = None, None
        # self.min = None
        self.size = 0
    
    class Node:
        def __init__(self, _key, _payload):
            self.key = _key
            self.payload = _payload
            self.degree = 0
            self.parent = self.child = self.left = self.right = None
            self.mark = False
    
    # function to iterate through a doubly linked list
    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag:
                break
            elif node == stop:
                flag = True
            yield node
            node = node.right

    def compareMin(self, x, y):
        if x.key > y.key:
            return y
        elif x.key == y.key:
            if len(x.payload)>len(y.payload):
                return y
            elif len(x.payload) == len(y.payload):
                if x.payload[0] > y.payload[0]:
                    return y
        return x

    def insert(self, key, payload):
        node = self.Node(key, payload)
        node.left = node.right = node
        self.mergeToRootList(node)

        if self.min is None:
            self.min = node
        # update min
        else:
            if self.compareMin(self.min, node) is not self.min:
                self.min = node
        
        self.size += 1

    def extractMin(self):
        x = self.min

        if x.child is not None:
            if x.right is not None:
                self.rootHead = self.rootHead.right
                children = [_ for _ in self.iterate(x.child)]
                for i in range(len(children)):
                    self.mergeToRootList(children[i])
                    children[i].parent = None 
            else:
                self.rootHead = x.child

        self.removeFromRootList(x)

        # set new min
        if x == x.right:
            self.min = self.rootHead = None
        else:
            self.min = x.right
            self.consolidate()

        self.size -= 1
        return x

    def consolidate(self):
        A = [None] * (int(math.log2(self.size))+ 1)

        rootNodes = [_ for _ in self.iterate(self.rootHead)]

        for w in range(len(rootNodes)):
            x = rootNodes[w]
            d = x.degree
            
            while A[d] is not None:
                y = A[d]
                if self.compareMin(x, y) is not x:
                    temp = x
                    x, y = y, temp

                self.binomialMerge(y, x)
                A[d] = None
                d += 1
            
            A[d] = x

        # update new min
        for i in range(len(A)):
            if A[i] is not None:
                if self.compareMin(self.min, A[i]) is not self.min:
                    self.min = A[i]

    def binomialMerge(self, y, x):
        self.removeFromRootList(y)
        y.right = y.left = y
        y.parent = x
        self.mergeSiblings(x, y)
        x.degree += 1
        y.mark = False

    def mergeSiblings(self, parent, node):
        if parent.child is None:
            parent.child = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def mergeToRootList(self, node):
        if self.rootHead == None:   # check here
            self.rootHead = node
        else:
            node.right = self.rootHead.right
            node.left = self.rootHead
            self.rootHead.right.left = node
            self.rootHead.right = node

    # remove a node from the doubly linked root list
    def removeFromRootList(self, node):
        if node == self.rootHead:
            self.rootHead = node.right
        
        node.left.right = node.right
        node.right.left = node.left

# x = FibonacciHeap()

# x.insert(0.4, "a")
# x.insert(0.2, "b")
# x.insert(0.2, "c")
# x.insert(0.1, "d")
# x.insert(0.1, "e")
# print(x.extractMin().payload)
# print(x.extractMin().payload)
# print(x.extractMin().payload)
# print(x.extractMin().payload)
# print(x.extractMin().payload)
