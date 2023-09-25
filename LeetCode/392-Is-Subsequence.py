import bisect
from collections import defaultdict


class Solution:

    '''
    SKIPPED:
        Recursive Greedy Solution
            Two Pointer solution is objectively easier and better
        Dynamic Programming (Levenshtein Distance)
            Way too overkill
    '''

    '''
    Two Pointers
        An early fail check would be if len(s) > len(t)
        Keep two pointers, one starting at s[0] and the other at t[0]
        Iterate until either pointer exceeds the string len they are pointing to
            If the letters at both indices are the same, that letter in t is considered as part of the subsequence
                increment both i and j
            Otherwise, consider as in-between letter
                increment j only
        If at the end of the loop, i has reached len(s), all characters in s were accounted for
            return true
        Otherwise
            return false
    
    Is this greedy approach guaranteed to be optimal and correct?
        To prove the correctness of greedy algorithms, often we apply the contradiction technique, 
          i.e. deriving a contradicted fact while assuming the alternative argument is correct.
        It could be tedious to give a rigid mathematical proof on why the greedy algorithm is correct here. 
        Here we would like to present simply two arguments without detailed proofs:
            If the source is not a subsequence of the target string,
              in no case will our greedy algorithm return a positive result.
            If the source is indeed a subsequence of the target string (there could exist multiple solutions), 
              then our greedy algorithm will return a positive result as well. 
        For an obvious reason, our greedy algorithm does not exhaust all possible matches. However, one match suffices.

    If T -> len(t)
    Time:  O(T)
    Space: O(1)
    '''
    def isSubsequence(self, s: str, t: str) -> bool:
        # len of s and t
        ns, nt = len(s), len(t)
        # early reject: s cannot be a subsequence of t if len(s) > len(t)
        if ns > nt:
            return False
        
        # the pointers
        i, j = 0, 0
        while i < ns and j < nt:
            # on match increment pointer to s
            if s[i] == t[j]:
                i += 1
            # increment pointer to t regardless
            j += 1
        
        # if s pointer went past the end of s, we were successfully able to match all letters of s
        return i == ns
    
    '''
    Hashmap + Binary Search
        The idea is that the two pointer method iterates over t for every s
        We want to reduce that repeated work
        Therefore, we make a hashmap of t for char -> list[indexes]
        Not only does this immediately tell us if s had a non-t char (rejection),
          it also helps us find the next index of t that matches much faster than two pointers ever could
          using binary search. [O(log T) vs O(T)]
        
        First we start by making a hashmap of t for char -> list[indexes]
        Iterate for every string
            If the length of string > length of t, reject immediately
            We start a idx_of_t_matching_s idx with value -1
            Iterate over every character of string
                If a character is not in the hashmap, reject immediately
                Else find the lowest idx in the hashmap such that key = string char and idx > curr idx
                    This is done using binary search, the easiest way is to use bisect
                    (You may want to switch this out for your own implementation for interview purposes,
                      but I'm not going to do so because this is a follow-up)
                IF you could not find one, reject string
                Otherwise if you went through all letters of string, accept it
    
    Let N -> number of strings,
        S -> length of average string (or max string),
        T -> length of t
    Then,
    Time:  O(T + S log T)
        making the hashmap                                      O(T)
        finding if subsequence using hashmap (single string)    O(S log T)
            O(S) for iteration
            O(log T) for binary search on every iteration
    Space: O(T) [for hashmap]
    '''
    def isSubsequenceFollowup(self, strings: list[str], t: str) -> list[bool]:
        # creating the hashmap of t for char -> list[indexes]
        char_idxs = defaultdict(list)
        for i, c in enumerate(t):
            char_idxs[c].append(i)

        def isSubsequenceUsingLetterMap(s: str) -> bool:
            nonlocal char_idxs, t
            # early reject: s cannot be a subsequence of t if len(s) > len(t)
            if len(s) > len(t):
                return False
            
            # the index of t that s has matched until
            idx_of_t_matching_s = -1
            for c in s:
                # early reject: if s has a char t has never seen
                if c not in char_idxs:
                    return False
                
                # indexes of the char c in t
                idxs_of_c_in_t = char_idxs[c]
                # find the smallest index of t that has char c and is strictly greater than idx_of_t_matching_s
                match_idx = bisect.bisect_right(idxs_of_c_in_t, idx_of_t_matching_s)
                # if we couldn't find one, reject
                if match_idx == len(idxs_of_c_in_t):
                    return False
                
                # otherwise modify idx_of_t_matching_s to the index that was found
                idx_of_t_matching_s = idxs_of_c_in_t[match_idx]
            
        
        return [isSubsequenceUsingLetterMap(s) for s in strings]
