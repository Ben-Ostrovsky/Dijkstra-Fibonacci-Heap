import collections
from errno import ERANGE
import math


class Solution(object):
    def networkDelayTime(self, times, N, K):
        K -= 1
        graph = collections.defaultdict(list)
        for u, v, w in times:
            graph[u - 1].append((v - 1, w))

        FAIZ = (1 + math.sqrt(5)) / 2
        nodes = [None] * N

        class node(object):
            def __init__(self, i, value):
                self.i = i
                self.val = value
                self.degree = 0
                self.left = self
                self.right = self
                self.parent = None
                self.child = None
                self.marked = False
                nodes[i] = self

        def addNode(nd, dbn):  # dbn for 'a node in the double-linked list'
            nd.left = dbn.left
            dbn.left.right = nd
            nd.right = dbn
            dbn.left = nd

        def heapPush(nd):
            addNode(nd, self.minNode)

        # we should refresh self.minNode and self.nodeCount every time we push something in, but no need here

        def removeNode(nd):
            nd.left.right = nd.right
            nd.right.left = nd.left

        def heapPop():
            # we should first check whether the heap is empty, but no need here
            ret = (self.minNode.i, self.minNode.val)
            mnd = self.minNode
            if mnd.child:
                cur = mnd.child
                while cur:
                    child = cur
                    cur.parent = None
                    removeNode(cur)
                    cur = None if cur.right == cur else cur.right
                    heapPush(
                        child
                    )  # use addNode(nd, self.minNode) if you want to use push to count nodes
            removeNode(
                mnd
            )  # we whould also check whether the heap is empty now, but no need now
            self.minNode = mnd.right
            A = [None] * (int(math.log(self.nodeCount, FAIZ)) + 1)
            while self.minNode:
                x = self.minNode
                removeNode(x)
                self.minNode = None if x.right == x else x.right
                x.left = x.right = x
                d = x.degree
                while A[d]:
                    y = A[d]
                    if x.val > y.val:
                        x, y = y, x
                    removeNode(y)
                    if x.child:
                        addNode(y, x.child)
                    else:
                        x.child = y
                    y.parent = x
                    x.degree += 1
                    y.marked = False
                    A[d] = None
                    d += 1
                A[d] = x
            for nd in A:
                if nd:
                    if self.minNode:
                        heapPush(
                            nd
                        )  # use addNode(nd, self.minNode) if you want to use push to count nodes
                        if nd.val < self.minNode.val:
                            self.minNode = nd
                    else:
                        self.minNode = nd
            self.nodeCount -= 1
            return ret

        def cut(child, parent):
            parent.degree -= 1
            parent.child = None if child.right == child else child.right
            child.parent = None
            removeNode(child)
            child.left = child.right = child
            child.marked = False
            heapPush(
                child
            )  # use addNode(nd, self.minNode) if you want to use push to count nodes

        def cascadingCut(parent):
            pp = parent.parent
            if pp:
                if parent.marked:
                    cut(parent, pp)
                    cascadingCut(pp)
                else:
                    parent.marked = True

        def decrease(node, time):
            # we should first check whether time is lesser than node.val, but no need now
            node.val = time
            parent = node.parent
            if parent and parent.val > node.val:
                cut(node, parent)
                cascadingCut(parent)
            if node.val < self.minNode.val:
                self.minNode = node

        dist = [float("inf")] * N
        dist[K] = 0
        prev = [None] * N
        self.minNode = node(K, 0)
        for i in xrange(N):
            if i != K:
                heapPush(node(i, dist[i]))
        self.nodeCount = N
        while self.nodeCount:  # ensures that the heap is always not empty to pop
            (
                source,
                time,
            ) = (
                heapPop()
            )  # if we just want to find the shortest path to a certain destination (D), we can break here if source == D
            for d, t in graph[source]:
                alt = time + t
                if alt < dist[d]:
                    dist[d] = alt
                    prev[d] = source  # recording the path
                    decrease(nodes[d], alt)
        mx = max(dist)
        return -1 if mx == float("inf") else mx
