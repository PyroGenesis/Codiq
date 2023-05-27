# The knows API is already defined for you.
# return a bool, whether a knows b
def knows(a: int, b: int) -> bool:
    # defined by LeetCode
    raise NotImplementedError()

class Solution:
    def findCelebrity(self, n: int) -> int:
        return self.findCelebrityGreaterDeduction(n)
    
    '''
    Greater deduction: Logical deduction + verification without caching or repeated calls
    
    Logical deduction (similar explanation as below solution)
        Let's us say we call knows(a, b) [where a != b]. We have 2 cases
        - knows(a, b) is False. This means that b cannot be a celeb because a doesn't know them
        - knows(a, b) is True.  This means that a cannot be a celeb because a knows someone else
        In both cases, you can see that we can rule out one of the candidates as a celeb.
        
        Therefore, if we select our knows() calls carefully, we can eliminate all but one of the people as celebs
            in (n-1) knows() calls [OR n-1 edges]
        
    Verification
        After we're done narrowing down our candidate, we can also make some additional assumptions while verifying whether
            the candidate is a true celebrity:
        
        While verifying that candidate knows no-one else
            We can assume that candidate knows no-one after themself because if they did, they would've been replaced by some other person
            Therefore, we only need to check that the candidate doesn't know anyone before themself
        
        While verifying that candidate is known by everyone
            If the current candidate was selected by a candidate switch, we know that the prev candidate knows current candidate
            Thereby we can reduce our calls for this verification to (n-2) [-1 for prev -> cand] [-1 for cand -> cand]
        
        Using these assumptions, we will never do a duplicate knows() call
    
    Time:  O(n)
    Space: O(1)
    '''
    def findCelebrityGreaterDeduction(self, n: int) -> int:
        # start with picking any person as a celeb
        prev_celeb, potential_celeb = 0, 0
        
        # narrowing down to one potential celeb
        for i in range(1, n):
            # We do not test below condition as every knows() tested has been done with a person with a diff idx
            # if i == potential_celeb:
            #     continue
            
            # eliminating one of the people based on knows() result and setting the other one as the potential celeb
            # the one eliminated is saved to save one future knows() call
            if knows(potential_celeb, i):
                prev_celeb, potential_celeb = potential_celeb, i
        
        # We've narrowed down our search and also established that potential_celeb does not know anyone after it
        # But what about people before the celeb? Let's verify celeb doesn't know anyone before themself either
        for j in range(potential_celeb):
            # If potential_celeb knows anyone before themself, it's a fail
            if knows(potential_celeb, j):
                return -1
        
        # Now, we need to know if everyone knows celeb
        # The only exception is prev_celeb, who we know knows potential_celeb, so we skip that one check
        for k in range(n):
            # skip if the check is with themself or the prev_celeb
            if k == potential_celeb or k == prev_celeb:
                continue
            # If potential_celeb is not known by someone, it's a fail
            if not knows(k, potential_celeb):
                return -1
        
        # potential_celeb passed every check, they are a true celeb
        return potential_celeb
    
    
    '''
    Logical deduction + Caching
    
    Logical deduction (same explanation as below solution)
        Let's us say we call knows(a, b) [where a != b]. We have 2 cases
        - knows(a, b) is False. This means that b cannot be a celeb because a doesn't know them
        - knows(a, b) is True.  This means that a cannot be a celeb because a knows someone else
        In both cases, you can see that we can rule out one of the candidates as a celeb.
        
        Therefore, if we select our knows() calls carefully, we can eliminate all but one of the people as celebs
            in (n-1) knows() calls [OR n-1 edges]
        
        In the end, we will be left with a single candidate and we can run a brute-force verification on that candidate
            to figure out whether a celeb exists or not
        
    Caching
        When we are narrowing down our candidate, all of our knows() calls are unique
        Let's look at the step where we verify whether the last candidate is a celeb. Is there any call overlap?
            Yes! The narrow-down operation would have used some calls which can be useful in the verification step but are not reused
        
        The lower the number of the celebrity candidate, the more of these duplicated calls there will be, 
            because the celebrity candidate spent longer in the potential_celeb variable, 
            and so was involved in a lot more of the initial "questioning".
        
        So we can wrap the knows call around a dict (OR use @lru_cache) to make sure all knows() calls are done at max once.
        This will increase our space complexity but will reduce the constant multiplier on the time complexity which might
            be useful if a knows() call is really expensive
    
        Time:  O(n)
        Space: O(n)
    '''
    def findCelebrityDeductionAndCaching(self, n: int) -> int:
        # start with picking any person as a celeb
        potential_celeb = 0
        
        # this caches all previous calls to knows() which might be useful later
        cache = {}
        # wrapper around knows() which makes use of the cache
        def knowsEx(a, b):
            nonlocal cache
            if (a, b) not in cache:
                cache[(a, b)] = knows(a, b)
            return cache[(a, b)]
                
        # Quick fn to confirm if any person is a celeb
        # This is run after we have narrowed down our candidates to a single person
        def isCeleb(celeb):
            for i in range(n):
                # Do not compare a person to themselves
                if i == celeb: continue
                # if they know someone or are not known by someone, they are not a celeb
                # uses the knowsEx() wrapper to reuse old calls
                if knowsEx(celeb, i) or not knowsEx(i, celeb):
                    return False
            # they know no-one and everybody knows them, that is a celeb
            return True
        
        # narrowing down to one potential celeb
        for i in range(1, n):
            # We do not test below condition as every knows conn tested has been done with a person with a diff idx
            # if i == potential_celeb:
            #     continue
            
            # eliminating one of the people based on knows() result and setting the other one as the potential celeb
            if knowsEx(potential_celeb, i):
                # now if the potential_celeb changed, our cache is no longer useful (since we will potentially verify the new candidate)
                #   so we reset it
                cache = { (potential_celeb, i): True }
                potential_celeb = i
        
        # verifying whether our potential celeb is actually a celeb and returning the result
        return potential_celeb if isCeleb(potential_celeb) else -1
    
    
    '''
    Logical deduction
        Let's us say we call knows(a, b) [where a != b]. We have 2 cases
        - knows(a, b) is False. This means that b cannot be a celeb because a doesn't know them
        - knows(a, b) is True.  This means that a cannot be a celeb because a knows someone else
        In both cases, you can see that we can rule out one of the candidates as a celeb.
        
        Therefore, if we select our knows() calls carefully, we can eliminate all but one of the people as celebs
            in (n-1) knows() calls [OR n-1 edges]
        
        In the end, we will be left with a single candidate and we can run a brute-force verification on that candidate
            to figure out whether a celeb exists or not
        
        Time:  O(n)
        Space: O(1)
    '''
    def findCelebrityDeduction(self, n: int) -> int:
        # start with picking any person as a celeb
        potential_celeb = 0
        
        # Quick fn to confirm if any person is a celeb
        # This is run after we have narrowed down our candidates to a single person
        def isCeleb(celeb):
            for i in range(n):
                # Do not compare a person to themselves
                if i == celeb: continue
                # if they know someone or are not known by someone, they are not a celeb
                if knows(celeb, i) or not knows(i, celeb):
                    return False
            # they know no-one and everybody knows them, that is a celeb
            return True
        
        # narrowing down to one potential celeb
        for i in range(1, n):
            # We do not test below condition as every knows() tested has been done with a person with a diff idx
            # if i == potential_celeb:
            #     continue
            
            # eliminating one of the people based on knows() result and setting the other one as the potential celeb
            if knows(potential_celeb, i):
                potential_celeb = i
        
        # verifying whether our potential celeb is actually a celeb and returning the result
        return potential_celeb if isCeleb(potential_celeb) else -1
        
    '''
    Skipped:
        2-pointer solution: Slightly worse than Logical Deduction
    '''
        
    '''
    Brute force - TLE
    '''
    def findCelebrityBruteForce(self, n: int) -> int:
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if knows(i, j):
                    break
            else:
                for k in range(n):
                    if not knows(k, i):
                        break
                else:
                    return i
        return -1
