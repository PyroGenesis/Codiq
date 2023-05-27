class Solution:
    '''
    Math
    Don't use your head too much here, just go through appropriate examples and find the pattern    
    ┌─────┬──────┬─────────┬───────────┬────────────┬───────────┬────────────┬─────────────┐
    │ low │ high │  odds   │ odd count │ high - low │ diff // 2 │ low is odd │ high is odd │
    ├─────┼──────┼─────────┼───────────┼────────────┼───────────┼────────────┼─────────────┤
    │   3 │    7 │ [3,5,7] │         3 │          4 │         2 │ Yes        │ Yes         │
    │   3 │    8 │ [3,5,7] │         3 │          5 │         2 │ Yes        │ No          │
    │   2 │    8 │ [3,5,7] │         3 │          6 │         3 │ No         │ No          │
    │   3 │    6 │ [3,5]   │         2 │          3 │         1 │ Yes        │ No          │
    │   4 │    6 │ [5]     │         1 │          2 │         1 │ No         │ No          │
    └─────┴──────┴─────────┴───────────┴────────────┴───────────┴────────────┴─────────────┘
    The formula comes out to be:
        odds = [(high - low) // 2] + 1 if (low is odd OR high is odd)

    Time:  O(1)
    Space: O(1)
    '''
    def countOdds(self, low: int, high: int) -> int:
        odds = (high - low) // 2
        # num & 1 is just a quick way to check for odd value
        if low & 1 or high & 1:
            odds += 1
        return odds
