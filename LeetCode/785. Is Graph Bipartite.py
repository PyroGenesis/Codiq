from typing import List


class Solution:
    '''
    Skipped:
        BFS solution
        Union-find solution: https://leetcode.com/problems/is-graph-bipartite/discuss/1990681/python3-union-find
    '''
    def isBipartite(self, graph: List[List[int]]) -> bool:
        return self.isBipartiteDfsIterative(graph)
    
    
    '''
    DFS solution
    
        Time:  O(V + E) [we traverse every node and edge once]
        Space: O(V)     [storing colors for every node]
    '''
    def isBipartiteDfsIterative(self, graph: List[List[int]]) -> bool:
        # stores the color for every node we've processed
        # also acts as a de-facto visited checker
        node_color = {}
        
        # go through every node 
        # (because there might be disconnected subgroups that you'll miss if you only select one starting node)
        for node in range(len(graph)):
            # if a node is colored, it and all of its neighbors will already have been processed
            # so just skip it
            if node in node_color:
                continue
            
            # color the unseen node in the new subgraph
            node_color[node] = 0

            # stack to do DFS
            stack = [node]
            # do DFS while verifying every neighbor of a node respects its color
            while stack:
                stack_node = stack.pop()
                # inverting the color of the neighbor node 0->1 and 1->0
                neighbor_color = 1 - node_color[stack_node]
                
                # check if every neighbor satisfies the neighbor color property
                # also add them to the stack to be processed if they are not already colored
                for neighbor in graph[stack_node]:
                    if neighbor not in node_color:
                        # if the neighbor is not colored, we can color it and add it to the stack
                        stack.append(neighbor)
                        node_color[neighbor] = neighbor_color
                    elif node_color[neighbor] != neighbor_color:
                        # otherwise if the node is colored but it's not satisfying the color property, 2-coloring is impossible
                        return False
        
        # we have processed all nodes without failing
        return True

    def isBipartiteDfsRecursive(self, graph: List[List[int]]) -> bool:        
        # stores the color for every node we've processed
        # also acts as a de-facto visited checker
        node_color = {}

        def dfs(node: int, color: int) -> bool:
            nonlocal graph, node_color

            # if the node is colored but it's not satisfying the color property, 2-coloring is impossible
            if node in node_color:
                return node_color[node] == color
            
            # color current node
            # also marks it as visited
            node_color[node] = color
            
            # check if every adjacent node is colored correctly
            adjacent_color = 1 - color
            for adjacent in graph[node]:
                if not dfs(adjacent, adjacent_color):
                    return False
            
            # everything is colored correctly
            return True
                
        # go through every node 
        #   (because there might be disconnected subgroups that you'll miss if you only select one starting node)
        # for every node, 
        #   either it has to be already explored OR
        #   running dfs on it gives us a valid 2-coloring
        return all(node in node_color or dfs(node, 0) for node in range(len(graph)))
