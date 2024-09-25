import math
from typing import List

from LeetCode.CustomStructures import Trie

class Solution:
    '''
    SKIPPED:
        Substring solutions
    
    We want to find the least amount of leftover characters.
    Here, greedy solution will not work because it may be better to skip a character that is part of a word,
        so that the chars after it may be consumed by a bigger word.
    Example:
        "abcdefg"
        dictionary: ["abc", "bcdefg"]
            Here 'a' of "abc" needs to be skipped to match the longer "bcdefg"
        "abcdebd"
        dictionary: ["bcd", "bcde", "ebd"]
            Here, we get a better result if we match "bcd" instead of "bcde" (so that "ebd" matches)
    
    So for every letter, we decide if we want to pick it or skip it
        if we do pick it, we have to continue picking until we make the shortest word
            Again, here we have a decision whether to 
                continue consuming more characters to make a bigger word or stop here
        If we skip it, we can start again using next letter
    
    Do we use Dynamic Programming?
        Does the problem ask for a min, max, number of ways, etc?
            Yes, we need the min amount of leftover extra chars
        Do earlier decisions affect future decisions?
            Yes, as we saw in the examples
    
    Therefore we use Dynamic Programming
        Overlapping Subproblems:
            minExtraChar("abcdefg") can be broken down to:
                1 + minExtraChar("bcdefg") OR
                minExtraChar("defg")
        Optimal Substructure:
            If we know, the solutions to all s[i:] where 1 <= i < n,
            s[0:] can be computed in O(1)
    
    Trie is the perfect datastructure here, the only difference is whether our approach is top-down or bottom-up.
    Personally, I like the top-down approach more, and there is no difference in the time or space complexities.
    '''
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:
        return self.minExtraCharBottomUp(s, dictionary)
    

    '''
    Trie Bottom-UP
        An iterative dp solution using a Trie
        A state is identified by an index (start) in the string s
            it represents the number of extra chars in the string s[start:]
        Here, we iterate backwards through s index from n-1 to 0 inclusive
        Base case is start == n, in which case there can be no extra chars
        Another case is treating start char as an extra char, 
            in which case we increment the count and use the precomputed value dp[start + 1]
        Finally, try to consume chars to match a dictionary word
            Each time we hit a word boundary, 
                we can use the precomputed value dp[end+1], where end = start + len(word)
            Stop consuming on first mismatch
        We return dp[0]
    
        DP framework:
            State:
                The state is the remaining string s[i:] where 0 <= i < n
                    This can be represented by i
            Base case:
                If i == n, there can be no more extra chars, so return 0
            Recurrence relation:
                dp[i] = min(
                    1 + dp[i+1],
                    dp[i + len(word)] for word in dictionary if s[i : i+len(word)] == word 
                    (we do this part efficiently with a trie)
                )
    
    let n -> len(s)
        k -> number of words in dictionary
        m -> avg len of word in dictionary
    Time:  O(n^2 + k*m)
        Creating trie:          O(k*m)
        Computing each state:   O(n)
        States:                 n+1
    Space: O(n + k*m)
        trie:                   O(k*m)
        recursion:              O(n)
    '''
    def minExtraCharBottomUp(self, s: str, dictionary: List[str]) -> int:
        n = len(s)
        trie = Trie()
        # creating the trie
        for word in dictionary:
            trie.insert(word)
        
        # states can be stored in a simple array
        # we do n+1 to handle dp[n] case cleanly
        #   dp[n] = 0, because there are no chars left to be extra chars
        dp = [0]*(n+1)
        # since dp[i] can be computed if we know dp[1+1] ... dp[n], 
        #   we iterate backwards
        for start in range(n-1, -1, -1):
            # counting current char as extra char
            dp[start] = dp[start + 1] + 1
            # attempting to consume chars, start from root
            node = trie.root
            for end in range(start, n):
                c = s[end]
                if c not in node.children:
                    # quit immediately on mismatch
                    break
                node = node.children[c]
                if node.end:
                    # once we consume a complete word, 
                    #   we immediately know the rest of the extra chars as we have already precomputed 
                    #   the minimum number of extra chars when starting right after where the word consumed ends.
                    # we don't break here since we want to try consuming bigger words too
                    dp[start] = min(dp[start], dp[end+1])
        
        # the result is the minimum of extra chars when starting from index 0
        return dp[0]


    '''
    Trie Top-Down
        A memoized, recursive solution using a Trie
        A state is identified by an index (curr) in the string s
            it represents the number of extra chars in the string s[curr:]
        Base case is curr reaching n, in which case there can be no extra chars
            Also, if this index was processed before, simply use the previously calculated 
        Another case is treating curr char as an extra char, 
            in which case we increment the count and move on to the next char
        Finally, try to consume chars to match a dictionary word
            Each time you hit a word boundary, branch off another recursive call from the next index
            Stop consuming on first mismatch
    
        DP framework:
            State:
                The state is the remaining string s[i:] where 0 <= i < n
                    This can be represented by i
            Base case:
                If i == n, there can be no more extra chars, so return 0
            Recurrence relation:
                recurse(i) = min(
                    1 + recurse(i+1),
                    recurse(i + len(word)) for word in dictionary if s[i : i+len(word)] == word 
                    (we do this part efficiently with a trie)
                )
    
    let n -> len(s)
        k -> number of words in dictionary
        m -> avg len of word in dictionary
    Time:  O(n^2 + k*m)
        Creating trie:          O(k*m)
        Computing each state:   O(n)
        States:                 n+1
    Space: O(n + k*m)
        trie:                   O(k*m)
        recursion:              O(n)
    '''
    def minExtraCharTopDown(self, s: str, dictionary: List[str]) -> int:
        n = len(s)
        trie = Trie()
        # creating the trie
        for word in dictionary:
            trie.insert(word)
        
        # states can be stored in a simple array
        memo = [-1]*n
        def recurse(curr):
            nonlocal s, n, trie, memo
            if curr == n:
                # base case
                return 0
            if memo[curr] != -1:
                # using memoization
                return memo[curr]
            
            # counting current char as extra char
            non_dict_chars = 1 + recurse(curr+1)
            # attempting to consume chars, start from root
            node = trie.root
            for i in range(curr, n):
                c = s[i]
                if c not in node.children:
                    # quit immediately on mismatch
                    break
                node = node.children[c]
                if node.end:
                    # branch off recursion on word boundary
                    non_dict_chars = min(non_dict_chars, recurse(i+1))
            
            # store in memo
            memo[curr] = non_dict_chars
            return non_dict_chars
            
        return recurse(0)
