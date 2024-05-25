from collections import Counter


class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        return self.removeDuplicateLettersGreedyStack(s)
        
    '''
        Greedy solution with stack - Actually more understandable and also optimal
        Time:  O(n)
            (outer loop) * 26 (stack search) * 26 (inner while loop max pops) = O(n)
        Space: O(1)
            max stack size is 26
    '''
    def removeDuplicateLettersGreedyStack(self, s: str) -> str:
        # this will let us know if there are more instances of s[i] left in s after index i
        last_occurence = {ch: i for i, ch in enumerate(s)}
        curr_seq = []
        
        for i, ch in enumerate(s):
            # we can only try to add c if it's not already in our solution
            # this is to maintain only one of each character
            # since stack max size is 26, this can be said to be O(1)
            if ch not in curr_seq:
                
                # if the last letter in our solution:
                #    1. exists
                #    2. is greater than ch so removing it will make the string lexicographically smaller
                #    3. it's not the letter's last occurrence
                # we remove it from the solution to keep the solution optimal
                while curr_seq and curr_seq[-1] > ch and last_occurence[curr_seq[-1]] > i:
                    curr_seq.pop()
                
                # add curr char to solution
                curr_seq.append(ch)
                
        return ''.join(curr_seq)
        
        
    '''
        Pure Greedy solution - Confusing but valid
            Here, the intuition comes about when you try and figure out how to pick the first letter of our ans sequence
            Forget optimality for a second. What condition will ensure if a letter will be a valid first letter of a sequence containing all letters?
                Well, a letter is guaranteed to be a valid leftmost letter, if all unique letters (including itself) occur at least once in the string [letter_idx:n]
                A good way to implement this would be to keep a Counter of all letters at the start.
                As we iterate over the letters, we decrement the count of the letter in the Counter.
                When a letter hits the count of 0, no letter after this idx can be a valid leftmost letter because it won't have at least one unique letter.
            Now that we have figured out whether a letter will be a valid leftmost letter, how do we get the OPTIMAL valid leftmost letter?
                Simple, we iterate over all valid leftmost letters and pick the smallest one.

        Time:  O(n)
            Each recursive call will take O(n). 
            The number of recursive calls is bounded by a constant (26 letters in the alphabet), so we have O(n) * 26 = O(n).
        Space: O(n)
            Each time we slice the string we're creating a new one (strings are immutable).
            However we will only make a maximum of 26 slices, so we have O(n) * 26 = O(n).

    '''
    def removeDuplicateLettersGreedyButConfusing(self, s: str) -> str:
        # if we have less than 2 letters left, we pick them directly
        if len(s) < 2:
            return s
        
        counter = Counter(s)

        # find min_ch_idx_with_valid_suffix - the index of the leftmost letter in our solution
        # we create a counter and end the iteration once the suffix doesn't have each unique character
        # min_ch_idx_with_valid_suffix will be the index of the smallest character we encounter before the iteration ends
        min_ch_idx_with_valid_suffix = 0
        for i in range(len(s)):
            # if current char is better than our starting point, we set current as starting point
            # we know current as starting point will have a valid suffix because if not then atleast one counter value would've reached 0 before
            if s[i] < s[min_ch_idx_with_valid_suffix]:
                min_ch_idx_with_valid_suffix = i
            counter[s[i]] -= 1
            
            # one of the letters reached their last occurence, so we can no longer search for better chars to start from, we start from the best pos we found so far
            if counter[s[i]] == 0:
                break
        
        # our answer is the leftmost letter plus the recursive call on the remainder of the string
        # note we have to get rid of further occurrences of s[min_ch_idx_with_valid_suffix] to ensure that there are no duplicates
        return s[min_ch_idx_with_valid_suffix] + self.removeDuplicateLettersGreedyButConfusing(
            s[min_ch_idx_with_valid_suffix+1:].replace(s[min_ch_idx_with_valid_suffix], '')
        )
        
