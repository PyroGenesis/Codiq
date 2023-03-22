
import math
from typing import List

'''
Skipped:
    BFS
        Create adjacency list
        Create visit array / set
        run bfs using queue starting from node 1
          marking nodes as visited when encountered
        track min dist in this loop
        O(n + e), O(n + e)
    
    DFS
        Create adjacency list
        Create visit array / set
        run dfs using recursion starting from node 1
          marking nodes as visited when encountered
        track min dist in a global var
        O(n + e), O(n + e)
'''

'''
Optimized Union-Find / DSU
    Since we can repeat nodes and edges as much as we want,
      and we only care about the min edge crossed in the path
    This problem devolves to find the samllest edge in graph

    But there is a catch!
    The graph is not guaranteed to be completely connected.
    So the problem becomes to find the smallest edge in the subgraph that includes node 1 and n
    But since we are guaranteed a solution, node 1 and n have to be in the same connected graph
    So the problem becomes to find the smallest edge in the subgraph that includes node 1

    Now shift your perspective to that of the edges coming in
    When a new edge comes in, 
        we need to know if it will belong to the node 1 subgraph
        we also need to know if this edge connects another subgraph that has a smaller edge
    The DSU is the best data structure for these tasks!
    
    We implement the DSU with a modification to keep track of the smallest edge / score for every subgraph
    The score for every subgraph is kept in self.score[root of subgraph]
    It is updated on every union (every edge added)

    Time complexity: O(n + e)
        Create DSU of size n:   O(n)
        Loop for edges:         O(e)
            Optimized DSU       O(alpha(e)) = O(1)
    Space complexity: O(n) [for DSU]
'''
class ModifiedDsu:
    def __init__(self, n):
        self.parent = list(range(n))    # ith value is the parent node to node i
        self.rank = [1]*n               # max depth of subtree rooted here (used for union by rank)
        self.score = [math.inf]*n       # score for subgraph containing node i
    
    def find(self, x):
        # if the node is not its own parent, we need to recurse on parent
        if x != self.parent[x]:
            # path compression
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    # update the scores of the two subgraphs getting connected via edge with distance 'dist'
    def __updateScores(self, rootX, rootY, dist):
        score = min(self.score[rootX], self.score[rootY], dist)
        self.score[rootX] = score
        self.score[rootY] = score
    
    # returns a boolean whether or not union was needed 
    # not necessary to return boolean
    def union(self, x, y, dist):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            # no union needed
            # but this edge might have a low dist so update scores
            self.__updateScores(rootX, rootY, dist)
            return False

        if self.rank[rootX] > self.rank[rootY]:
            # rootX has deeper subtree, therefore set it as parent to rootY (and its subtree)
            self.parent[rootY] = rootX
        elif self.rank[rootX] < self.rank[rootY]:
            # rootY has deeper subtree, therefore set it as parent to rootX (and its subtree)
            self.parent[rootX] = rootY
        else:
            # both subtrees are of equal depth, therefore choose either one of them as the parent of the other
            # here we chose rootX as the parent of rootY, therefore rootX depth increases by 1
            self.parent[rootY] = rootX
            self.rank[rootX] += 1
        
        # union complete
        # we update the scores of both subgraphs (though we only really need to update the parent one)
        self.__updateScores(rootX, rootY, dist)
        return True
    
    # gets the score of the subgraph containing node 1
    def getMinScoreFromNode1(self):
        return self.score[self.find(1)]

class Solution:
    def minScore(self, n: int, roads: List[List[int]]) -> int:
        # initialize DSU
        dsu = ModifiedDsu(n+1)

        # add every edge, causing potential unions
        for x, y, dist in roads:
            dsu.union(x, y, dist)
        
        # return the smallest edge of the subgraph containing node 1
        return dsu.getMinScoreFromNode1()
