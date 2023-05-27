from collections import defaultdict
from typing import List

class Solution:
    def distinctNames(self, ideas: List[str]) -> int:
        return self.distinctNamesGroupByPrefix(ideas)

    '''
    First, read the explanation for distinctNamesGroupBySuffix() solution

    I was too hasty in discarding the other grouping strategy
        c -> offee      d -> onuts      t -> ime, offee

    If you look closely, a similar property emerges
    if the two sets of prefix-key values (sets of suffixes) have intersects, those can never be used to swap
    Also swapping prefixes of the same suffix is pointless, both swapped words will always be dups
    In the above example:
        {c -> offee} and {t -> ime, offee} have an intersection 'offee' so you can see all 'offee' swaps are invalid
        ("coffee", "time") -> invalid
        ("toffee", "time") -> invalid
    Multiply all combinations by 2 and you've got your answer!
    
    Note that any suffixes in the sets that do not intersect will form valid swaps
    Example 1:
        c -> offee, ake         t -> offee, ime
        valid swap: ake-ime,                        ans = 2
    Example 2:
        c -> offee, ake, old    t -> offee, ime, ap
        valid swap: ake-ime ake-ap old-ime old-ap,  ans = 8

    Even though this solution seems to be the same time-space complexity as GroupBySuffix,
      it performs better because
        1. We can make use of a list instead of dictionary for the keys which will give faster access
        2. Larger sets. GroupByPrefix will have 26 sets and GroupBySuffix had O(suffix) sets
            So I think the larger but fewer sets lead to lesser number of set operations and
            calculation with bigger numbers

    Let the number of words to be n
    Let the average length of a word to be m
    Time complexity: O(m * n)
        letter_idx: O(1)
        Hashing every suffix and adding them to a set: O(m*n)
            It takes O(m) time to hash a string of length m, 
            thus it takes O(n*m) time to hash and store n strings
        Now, in the worst case every suffix will be unique 
          so we will have 26 suffix sets with n/26 suffixes each
        Iterating loop: 26^2 = O(1)
        Set intersection: O(m*n)
            Because each set can have n/26 suffixes of m letters each
        Total: O(m*n + m*n) = O(m * n)
    Space complexity: O(m * n)
        We store all suffixes: n * (m-1)
    
    '''
    def distinctNamesGroupByPrefix(self, ideas: List[str]) -> int:
        letter_idx = {c: i for i, c in enumerate('abcdefghijklmnopqrstuvwxyz')}
        groups = [set() for _ in range(26)]
        companies = 0
        for idea in ideas:
            groups[letter_idx[idea[0]]].add(idea[1:])
        
        for i in range(26):
            for j in range(i+1, 26):
                mutual_count = len(groups[i] & groups[j])
                companies += (len(groups[i]) - mutual_count) * (len(groups[j]) - mutual_count) * 2

        return companies
    
    '''
    TLE
    You should be able to figure this solution with a single hint: Grouping
    There are only 2 real ways to group the data
        Take the example ["coffee","donuts","time","toffee"]
        1.  c -> offee      d -> onuts      t -> ime, offee
        2.  offee -> c,t    onuts -> d      ime -> t
    If you look closely at the 2nd grouping, a property emerges
    if the two sets of suffix-key values (sets of prefixes) have intersects, those can never be used to swap
    Also swapping prefixes of the same suffix is pointless, both swapped words will always be dups
    In the above example:
        {offee -> c,t} and {ime -> t} have an intersection 't' so you can see all 't' swaps are invalid
        ("coffee", "time") -> invalid
        ("toffee", "time") -> invalid
    Multiply all combinations by 2 and you've got your answer!
    
    Note that any letters in the sets that do not intersect will form valid swaps
    Example 1:
        offee -> c, t       ake -> b, t
        valid swap: c-b,    ans = 2
    Example 2:
        offee -> c, t, s    ake -> b, t, m
        valid swap: c-b s-b c-m s-m, ans = 8

    Final optimization:
        For getting the valid swaps between two groups, use
            mutual_count = len(prefix_sets[i] & prefix_sets[j])
            companies += (len(prefix_sets[i]) - mutual_count) * (len(prefix_sets[j]) - mutual_count) * 2
        instead of
            companies += len(prefix_sets[i] ^ prefix_sets[j]) * 2

    Let the number of words to be n
    Let the average length of a word to be m
    Time complexity: O(m*n + n^2) OR O(n * (m + n))
        Hashing every word and adding them to a set: O(m*n)
            It takes O(m) time to hash a string of length m, 
            thus it takes O(n*m) time to hash and store n strings
        Now, in the worst case every suffix will be unique 
          so we will have n/26 [O(n)] sets with 1-26 chars each
        Iterating through all sets: O(n^2)
        Set intersection: 26 = O(1)
        Total: O(m * n^2)
    Space complexity: O(m * n)
        We store all suffixes: n * (m-1)
    '''
    def distinctNamesGroupBySuffix(self, ideas: List[str]) -> int:
        companies = 0
        groups = defaultdict(set)
        for idea in ideas:
            groups[idea[1:]].add(idea[0])
        
        prefix_sets = list(groups.values())
        n = len(prefix_sets)
        for i in range(n):
            for j in range(i+1, n):
                mutual_count = len(prefix_sets[i] & prefix_sets[j])
                companies += (len(prefix_sets[i]) - mutual_count) * (len(prefix_sets[j]) - mutual_count) * 2

        return companies

    '''
    Check every combination of two words: TLE
    Optimization 1: Keep track of valid and invalid start letters for a particular idea to skip the checking every time.
    Optimization 2: Check for same starting char, in which case it is bound to be invalid.
    Iterating all possible values is just not fast enough, we need some calc to bypass the cost

    Let the number of words to be n
    Let the average length of a word to be m
    Time complexity: O(m * n^2)
        Iterating through every 2 word combination: O(n^2)
        Creating new word: O(m)
        Hashing the word: O(m)
    Space complexity: O(m * n^2)
        We keep track of all new words, valid or not
    '''
    def distinctNamesBruteForce(self, ideas: List[str]) -> int:
        idea_set = set(ideas)
        n = len(ideas)
        companies = 0

        valids = defaultdict(set)
        invalids = defaultdict(set)

        for i in range(n):
            idea_a_start = ideas[i][0]
            for j in range(i+1, n):
                idea_b_start = ideas[j][0]

                # if both are the same, simply raject
                if idea_a_start == idea_b_start:
                    continue
                
                # if any one of them are invalid, simply reject
                if idea_a_start in invalids[j] or idea_b_start in invalids[i]:
                    continue
                
                # fill in whichever one doesn't already have a valid record
                if idea_a_start not in valids[j]:
                    if (idea_a_start + ideas[j][1:]) not in idea_set:
                        valids[j].add(idea_a_start)
                    else:
                        invalids[j].add(idea_a_start)
                if idea_b_start not in valids[i]:
                    if (idea_b_start + ideas[i][1:]) not in idea_set:
                        valids[i].add(idea_b_start)
                    else:
                        invalids[i].add(idea_b_start)
                
                if idea_a_start in valids[j] and idea_b_start in valids[i]:
                    companies += 2
        
        return companies
