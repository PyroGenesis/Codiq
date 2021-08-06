# LeetCode imports
from LeetCode.GlobalStructures import NaryNode as Node
from typing import List
import collections

"""
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children
"""

class Solution:
    
    '''
        Skipped:
            I don't think any of these solutions are any more efficient or helpful
             than the simple basic one.
             
            Simplified BFS: Guide
            Recursion: Guide
    '''
    
    '''
        Initial, Optimal, Simple BFS
        BFS has level-order traversal in its definition
            Just do simple BFS
            Anything else is just overcomplicating the problem
        BFS algo:
            Set a queue (starting with single root node)
            while the queue has nodes
                Pop all existing nodes in queue (all of them will be in same level)
                    Keep track of which nodes were 'existing' by recording the len at
                     start of while loop
                Value of each node goes in a list created at start of while loop
                Children of each node go in the queue (for next level)
                When done with removing 'existing' nodes, add the value list to the master list
        
        Time:  O(n)
        Space: O(n)
    '''
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if not root:
            return []
        
        traversal = []                      # final list of values (level-ordered)
        queue = collections.deque([root])   # holds nodes per level
        
        # while we have a level to go
        while queue:
            # vars for this level
            level_len = len(queue)
            level_nodes = []
            
            # process all nodes of current level
            for _ in range(level_len):
                # remove the node, add its value to level list, add its children to queue
                node = queue.popleft()                
                if node.children:
                    queue.extend(node.children)
                level_nodes.append(node.val)
            
            # add all values of current level into final list
            traversal.append(level_nodes)
        
        return traversal