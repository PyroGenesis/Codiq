class Solution:
    '''
    Approach:
        Reading the problem, the solution seems simple but there are a lot of edge cases
        Let's first go through the approach, then we'll outline the edge cases

        Start by iterating through letters of both strings one by one and recording the differences
        If there are 2 differences, they should be a swappable pair
        If there are no differences, the string needs to have duplicate characters to swap
        Otherwise it is impossible to reconcile

    Edges cases to consider:
        - If the strings are not of equal length, that's an outright fail
        - If there are more than 2 differences, that's an early fail
        - The strings might be equal but not have any duplicate characters for the mandatory swap
        - The two string differences might not be mirrored
        - There might be a single differences

    Time:  O(n)
    Space: O(26) = O(1)
    '''
    def buddyStrings(self, s: str, goal: str) -> bool:
        # strings are not of equal lengths, so fail immediately
        if len(s) != len(goal):
            return False
        
        diffs = []
        for i, (a, b) in enumerate(zip(s, goal)):
            # record differences between the strings
            if a != b:
                diffs.append((a, b))
            
            # if there are more than 2 differences, fail early
            if len(diffs) > 2:
                return False
        
        if len(diffs) == 0:
            # if the strings are the same, the string needs at least 1 duplicate character
            return len(set(s)) < len(s)
        elif len(diffs) == 2:
            # if the strings have 2 differences
            # verify that the differences are mirrored
            (a1, b1), (a2, b2) = diffs
            return a1 == b2 and b1 == a2
        
        # any other scenario is a fail
        return False
