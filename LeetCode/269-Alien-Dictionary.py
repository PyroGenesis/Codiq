# LeetCode imports
from typing import List
import collections

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        # print(words, end=": ")
        n = len(words)
        if n==0: return 0
        if n==1: return ''.join(set(words[0]))
        
        # building the adjacency list
        graph = collections.defaultdict(list)
        for i in range(n-1):
            word1, word2 = words[i], words[i+1]
            j = 0
            difference = False
            for j in range(min(len(word1), len(word2))):
                c1, c2 = word1[j], word2[j]
                if c1 != c2:
                    graph[c1].append(c2)
                    difference = True
                    break
                else:
                    graph[c1]
            
            if not difference and len(word1) > len(word2):
                return ""
            
            for c in word1[j:]:
                graph[c]
            for c in word2[j:]:
                graph[c]
                
        
        # print(graph)
        
        ans = []
        # topo sort
        nodes = graph.keys()
        visited = {}
        
        def visit(node):
            nonlocal visited, ans, graph
            
            if node in visited:
                return visited[node]
            
            visited[node] = False
            for subnode in graph[node]:
                traverse = visit(subnode)
                if not traverse:
                    return False
            
            ans.append(node)
            visited[node] = True
            return True
        
        for node in nodes:
            if not visit(node):
                return ""
        
        return "".join(reversed(ans))
