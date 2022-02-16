from collections import Counter, defaultdict

class Solution:
    '''
    Optimized sliding window
        The concept is to make a sliding window across the container string (s2) which keeps a running hashmap synced with
            the hashmap of the contained string (s1)
        Base concept is to have a hashmap of s1 which will be our ground truth and a hashmap of our sliding window
            with the same size as s1
        Now if all char freq match between these two hashmaps, we have got a valid substring
        There are a few optimizations we do on top of the base concept
        * Keep a count of how many letters are at their correct frequency so we dont have to compare the entire hashmap of
            s1 on every letter consumed from s2. Instead you only need to check whether the char was/is the right freq
            before/after insertion/deletion from the sliding window
        * Quit when our sliding window start becomes so far ahead that there are not enough characters to make s1 from substring
        * If a letter occurs in s2 that isn't at all in s1, close the sliding window and start it again from the next character.
            This is because no substring with that character will ever be the answer
        
        Time: O(s2)
        Space: O(26) = O(1)
    '''
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1_len = len(s1)
        s2_len = len(s2)
        
        # if not possible due to contained size > container size
        if s1_len > s2_len:
            return False
        
        # initializations
        letters_matched = 0         # keeps counter of how many have a correct count between s1 and sliding window
        s1_letters = Counter(s1)    # the ground truth, ideal sliding window letter freq for a soln
        window = defaultdict(int)   # the sliding window
        i, j = 0, 0                 # the edges of the sliding window. One consumes, the other expels
        
        # since our sliding window has a fixed max / ideal size,
        # this is one of the rarer two pointer problems where we don't have to worry about the tail (j)
        # If we guarantee that the head doesn't go to the index where j can fail
        # we can omit the j cond entirely
        # Therefore, if this cond becomes false, there are too few chars left to create s1
        while (i + s1_len) <= s2_len:            
            ich = s2[i] # ith character
            jch = s2[j] # jth character
            
            # if any letter tried to get into sliding window which is not in s1,
            # we move the window to START from the next character
            if jch not in s1_letters:
                letters_matched = 0
                window.clear()
                i = j + 1
                j = j + 1
                continue
            
            # if it was the right count before insert we've lost a letter match
            if window[jch] == s1_letters[jch]:
                letters_matched -= 1
            # add jth letter
            window[jch] += 1
            # if it is the right count now after insert we've gained a letter match
            if window[jch] == s1_letters[jch]:
                letters_matched += 1
            
            window_len = (j+1) - i
            if window_len < s1_len:
                # window is too small, just expand it
                j += 1
            else:
                # this will be window_len == s1_len
                # window_len > s1_len is not possible, because with j += 1, comes i += 1
                
                # if all unique letters of s1 have matched, we have our solution
                if letters_matched == len(s1_letters):
                    return True
                
                # Else remove ith letter for upcoming window slide
                # if it was the right count before removal we've lost a letter match
                if window[ich] == s1_letters[ich]:
                    letters_matched -= 1
                # remove ith letter
                window[ich] -= 1
                # if it is the right count now after removal we've gained a letter match
                if window[ich] == s1_letters[ich]:
                    letters_matched += 1
                # Dont forget to increment these counters
                i += 1
                j += 1
        
        # no substring in sliding window matched
        return False
                
        
        '''
        Skipped:
            All the guide TLE solutions
            Non-optimized Array
            Non-optimized Sliding Window
        '''
        
            
        '''
        Old solution - Trades performance to gain simplicity
        Pretty good solution still
        '''
#     def checkInclusion(self, s1: str, s2: str) -> bool:
#         s1len = len(s1)
#         s2len = len(s2)
#         if s1len > s2len:
#             return False
        
#         orda = ord('a')
#         s1map = [0]*26
#         s2map = [0]*26
#         count = 0
        
#         for i in range(s1len):
#             s1map[ord(s1[i]) - orda] += 1
#             s2map[ord(s2[i]) - orda] += 1
        
#         for i in range(26):
#             if s1map[i] == s2map[i]:
#                 count += 1
        
#         l = 0
#         r = s1len
#         while r < s2len:
#             if count == 26:
#                 return True
#             lc = ord(s2[l]) - orda
#             rc = ord(s2[r]) - orda
            
#             s2map[lc] -= 1
#             if s2map[lc] == s1map[lc]:
#                 count += 1
#             elif s2map[lc] == s1map[lc]-1:
#                 count -= 1
                
#             s2map[rc] += 1
#             if s2map[rc] == s1map[rc]:
#                 count += 1
#             elif s2map[rc] == s1map[rc]+1:
#                 count -= 1
                
#             l += 1
#             r += 1
        
#         return count == 26
        