from collections import Counter, defaultdict

class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        return self.numberOfSubstringsFormula(s)

    '''
    Formula
        This solution is a logical extension of the last idea
        Recall that:
            1 occurrence = 1
            2 occurrence = 1 + 2 = 3
            3 occurrence = 1 + 2 + 3 = 6
        Following this logic,
            n occurrence = 1 + 2 + ... + n-1 + n
        This can be calculated using the summation formula:
            [n * (n+1)] / 2
        
        Another way to come to the same formula is that the number of substrings are:
            every combination of two of the same letters + count of that letter (for 1-substring)
        let x be number of 'a'
        =>  xC2 + x
        Extending this for all letters, we get
            nC2 + n
        =>  [n(n-1)]/2 + n
        =>  [n^2 - n + 2n] / 2
        =>  [n * (n+1)] / 2

        Yet another way to come to the same formula is to use the AP summation formula
            n/2 * [2a + (n-1)d]
        since a=1 and d=1
        =>  n/2 * [2 + n-1]
        =>  n/2 * (n+!)
        =>  [n * (n+1)] / 2
    
        let n -> number of chars in s
        Time:  O(n)
            Counting every character in s:  O(n)
            Looping through every freq:     O(26)
        Space: O(1)
            freq map = O(26) = O(1)
    '''
    def numberOfSubstringsFormula(self, s: str) -> int:
        # I'm using a dict here, you can use array[26] too
        # Counter is a shortcut, without it you would simply add up the freq of all letters first
        char_freq = Counter(s)

        # apply the formula for the freq of every letter
        # this can be done in a one-liner using the code below
        #   return sum((n*(n+1)) // 2 for n in char_freq.values())
        substring_count = 0
        for freq in char_freq.values():
            substring_count += (freq * (freq+1)) // 2
        return substring_count


    '''
    Counting characters
        The idea is to think about what happens to the number of substrings as we consume characters one by one.
        Now if we are taking the char 'a' into consideration, the number of substrings are the same whether
            its 'aa', 'axa' or 'fadsfasf'
        So for our observations, I'm ignoring other characters

        Observation:
        When string = 'xax',        substrings for 'a' = 1
             string = 'xaxax',      substrings for 'a' = 3 = 1+2 (a, axa, a)
             string = 'xaxaxax',    substrings for 'a' = 6 = 1+2+3 (a, axa, a, axaxa, axa, a)
        Every new occurrence of 'a' adds freq('a') substrings to our count
        Keeping this in mind, we iterate over s, keeping track of the count of letters
        Whenever we process a letter, we can simply add its freq to our total count
    
        let n -> number of chars in s
        Time:  O(n)
            Going through every character in s
        Space: O(1)
            freq map = O(26) = O(1)
    '''
    def numberOfSubstringsCount(self, s: str) -> int:
        # I'm using a dict here, you can use array[26] too
        # defaultdict is a shortcut, without it you would simply use a normal dict and an if condition
        char_freq = defaultdict(int)

        # adjust the counter as we encounter letters
        substring_count = 0
        for ch in s:
            char_freq[ch] += 1
            substring_count += char_freq[ch]
        return substring_count
