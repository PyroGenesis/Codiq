from typing import List

'''
Skipped:
    DFS / BFS
        Reject impossibility
        Create adjacency list
        Create visit array / set
        Initialize disconnected components to 0
        loop every node
            if not visited
                increment disconnected components
                use dfs / bfs to mark all nodes in that component as visited
        We'll have the value of all disconnected components in the end
        O(n + e), O(n + e)
'''

from LeetCode.CustomStructures import DSU
# You actually need to implement DSU here
'''
Optimized Union-Find / DSU
    First of all, the question of possibility
        a graph with n nodes will need n-1 edges at the minimum
        any lower and its impossible to include all nodes
        if n-1 or above, we can redistribute the edges as we see fit to connect all nodes
    Therefore if nodes > connections+1, it is impossible
    Otherwise it is guaranteed to be possible

    Next, if you look at the problem carefully, you'll see that we don't really care about which edges get moved
    We only care about how MANY need to be moved
    Also, by intuition, every disconnected node will require 1 edge to connect to the 'master' component
    But also, there might be components that are disconnected which also require 1 edge
    Therefore, our required answer is the number of disconnected components - 1

    Now guess, which data structure is the MVP in tracking connected and unconnected components?
    You're right, its the DSU
    We implement the base DSU, and start with n disconnected components
    With every connection, we check if it causes a union to occur
        If so, the number of disconnected components gets decremented
    In the end, we're left with the number of disconnected components and we return that minus 1

    Let e -> number of connections

    Time Complexity: O(n + e)
        Creating DSU:                       O(n)
        Loop                                O(e)
            for every edge e
            union operation: O(alpha(e)) = O(1)
    
    Space complexity: O(n)
        Space needed for DSU:               O(n)
'''
class Solution:
    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        if n > len(connections)+1:
            return -1
        
        dsu = DSU(n)
        disconnected_networks = n
        for a, b in connections:
            if dsu.union(a, b):
                disconnected_networks -= 1
        
        return disconnected_networks-1