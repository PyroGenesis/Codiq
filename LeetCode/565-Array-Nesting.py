# LeetCode imports
from typing import List


class Solution:
    def arrayNestingInitialDFS(self, nums: List[int]) -> int:
        '''
        Initial DFS solution
        '''
        # I have to basically do path compression from say DSU
        # I'm on the 4th version
        
        n = len(nums)
        longest_chain = 1 # because a min chain of 1 will always happen
        chain_lens = [0]*n
        
        def nestArrayLen(loc, og=None):
            nonlocal nums, chain_lens
            
            if chain_lens[loc] > 0:
                return chain_lens[loc]
            
            if nums[loc] == og:
                chain_lens[loc] = 1
                return 0
            
            if og is None:
                og = nums[loc]
            
            chain_lens[loc] = 1 + nestArrayLen(nums[loc], og)
            return chain_lens[loc]
        
        for i in range(n):
            if nums[i] == i:
                chain_lens[i] = 1
                continue
            if chain_lens[i] > 0:
                # this num is already visited
                continue                
                
            chain_lens[i] = nestArrayLen(i)
            longest_chain = max(longest_chain, chain_lens[i])
            
            # Just an optional small optimization:
            # if maximum is at least half of size of the array,
            # there can be no chain longer than it
            if longest_chain >= n / 2:
                return longest_chain
        return longest_chain
    
    def arrayNestingClean(self, nums: List[int]) -> int:
        n = len(nums)
        longest_chain = 1
        visited = set()
        
        for i in range(n):
            if i in visited:
                continue
            
            node = nums[i]
            chain_len = 0
            is_looped = False
            
            # we loop from node 2, 3, ... loop-1, lopp, 1
            while not is_looped:
                node = nums[node]
                chain_len += 1
                visited.add(node)
                is_looped = node == nums[i]
            
            longest_chain = max(longest_chain, chain_len)
            
            # Just an optional small optimization:
            # if maximum is at least half of size of the array,
            # there can be no chain longer than it
            if longest_chain >= n / 2:
                return longest_chain
        return longest_chain
    
    '''
    Skipped
        DSU with max component size tracking
            https://leetcode.com/problems/array-nesting/solution/1068905
            O(n)
    '''
    
    def arrayNestingOptimal(self, nums: List[int]) -> int:
        n = len(nums)
        longest_chain = 1
        
        for i in range(n):
            if nums[i] == -1:
                continue
            
            node = nums[i]
            chain_len = 0
            is_looped = False
            
            # we loop from node 2, 3, ... loop-1, lopp, 1
            while not is_looped:
                # print(i, node, nums[node], nums)
                # WARNING: Comma separated assignment doesn't work as intended when dealing with array indices
                # https://stackoverflow.com/a/55954971
                # That's why the below statement won't work
                #       node, nums[node] = nums[node], -1
                temp = node
                node = nums[node]
                nums[temp] = -1
                chain_len += 1
                is_looped = nums[node] == -1
            
            longest_chain = max(longest_chain, chain_len)
            
            # Just an optional small optimization:
            # if maximum is at least half of size of the array,
            # there can be no chain longer than it
            if longest_chain >= n / 2:
                return longest_chain
        return longest_chain
            
        
    def arrayNesting(self, nums: List[int]) -> int:
        return self.arrayNestingOptimal(nums)