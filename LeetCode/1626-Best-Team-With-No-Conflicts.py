from typing import List


class Solution:
    def bestTeamScore(self, scores: List[int], ages: List[int]) -> int:
        return self.bestTeamScoreIterativeDP(scores, ages)
    
    '''
    Now that you've understood the recursive logic, you need to change the perspective a little to understand iterative DP
    Understanding the sort
        First we need to clarify the major benefit of the sort
        The sort of tuples (age, score) completely eliminates the age parameter from our logic. This is how:
        All scores will be in a non-decreasing order except when age changes
        So if curr score > prev score, curr age >= prev age (because of sort) so we can happily take the player in the team
        This reduces our problem to finding the best non-decreasing (ascending) subsequence of scores

    Iterative logic
        First we sort our input according to (age, score)
        Now consider 1 player (the first):
            In this case, we simply take the player and leave dp[0] unchanged (player 1 score)
        Now player 2 is added:
            Scenario 1: player 2 score < player 1
                Because of our sort, this also means that player 2 age > player 1 and so they cannot exist in the same team
                dp[1] will remain unchanged (player 2 score)
            Scenario 2: player 2 score >= player 1
                Our sort makes age irrelevant, player 2 can happily take player 1 in their team
                dp[1] will be the max of dp[1] (player 2 score) and (player 2 + player 1 team score)
        At this stage,  dp[0] has the best team score for a team containing player 1 and 
                        dp[1] has the best team score for a team containing player 2 (+ earlier)
        Next player 3 is added: 
            Scenario 1: player 3 score < player 1
                Because of our sort, this also means that player 3 age > player 1 and so they cannot exist in the same team
                dp[2] will remain unchanged (player 3 score)
            Scenario 2: player 3 score >= player 1
                Our sort makes age irrelevant, player 3 can happily take player 1 in their team
                dp[2] will be the max of dp[2] (player 3 score) and (player 3 + player 1 team score)
            Scenario 3: player 3 score < player 2
                Because of our sort, this also means that player 3 age > player 2 and so they cannot exist in the same team
                dp[2] will remain unchanged (best score considering player 3 and player 1's team)
            Scenario 4: player 3 score >= player 2
                Our sort makes age irrelevant, player 3 can happily take player 2 (and their team) in their team
                dp[2] will be the max of dp[2] (score considered with player 1) and (player 3 + player 2 team score)
        After this  dp[2] will have the best team score containing player 3 and
                    dp[0], dp[1] will have the best team score not containing player 3
        So you can see how we can extend this logic to finally get the best team score overall
    '''
    def bestTeamScoreIterativeDP(self, scores: List[int], ages: List[int]) -> int:
        n = len(scores)
        # sanity check
        if n == 1:
            return scores[0]
        
        players = [(ages[i], scores[i]) for i in range(n)]
        players.sort()

        dp = [player[1] for player in players]

        for curr in range(1, n):
            for other in range(curr):
                if players[curr][1] >= players[other][1]:
                    dp[curr] = max(dp[curr], players[curr][1] + dp[other])
        
        return max(dp)


    '''
    First I did recursive with a scores[] as one of the params, returning sum(scores) at the end
    Then I did recursive while returning the score directly, returning 0 at the end
        This was done so that each recursive call becomes an independent subproblem and
          future scores could be cached
    Then I memoized the results of the recursive call using a dict[(idx, max_score)] cache
    Lastly, I realized (by reading the solution) that the cache can be more optimized
        Consider the picks (index) (0,1,3...) (0,2,3...)
            Now if we assume that only indices 1 and 2 conflict with each other, 
              there will still be separate memos for all entries for indices 3 and beyond because of the different max_score
            So if we just stored the conflicting index (say 3), we could more efficiently memoize future subproblems
        But how do we know exactly which index will conflict in the future?
            First, consider what each recurse call represents.
            Each call represents a state where all the previous choices are part of a valid team
              (and we're looking for more team members)
            Now let's say there is a future member that causes a conflict with a current user
                Let's quantify that as member x for chosen members [idx1 ... x ... idxn]
            Since all new members are chosen only if they have a equal score or higher than all previous members,
              this new member will also conflict with x+1 member, x+2 member .... idxn member
            Therefore we can simply keep track of the index of last member chosen to check for any future conflicts
        So if we reduce the memo scope from (idx, max_score) to (idx, last_idx), we can reduce
          space complexity and redundant subproblems significantly.
        Also, we need to change the dict memo to a 2d array memo to save performance on lookups
    '''
    def bestTeamScoreRecursiveDP(self, scores: List[int], ages: List[int]) -> int:
        n = len(scores)
        # sanity check
        if n == 1:
            return scores[0]
        
        players = [(ages[i], scores[i]) for i in range(n)]
        players.sort()

        memo = [[-1 for _ in range(n)] for _ in range(n)]
        def recurse1(i: int, scores: List[int], max_score: int) -> int:
            nonlocal n, players
            if i == n:
                return sum(scores)
            
            curr_player = players[i][1]

            take = 0
            if curr_player >= max_score:
                # take this player
                take = recurse1(i+1, scores + [curr_player], curr_player)
            # skip this player
            skip = recurse1(i+1, scores, max_score)

            return max(take, skip)

        def recurse2(i: int, max_score: int) -> int:
            nonlocal n, players
            if i == n:
                return 0
            
            curr_player = players[i][1]

            take = 0
            if curr_player >= max_score:
                # take this player
                take = curr_player + recurse2(i+1, curr_player)
            # skip this player
            skip = recurse2(i+1, max_score)

            return max(take, skip)
        
        def recurse3(i: int, max_score: int) -> int:
            nonlocal n, players, memo
            if i == n:
                return 0
            if (i, max_score) in memo:
                return memo[(i, max_score)]
            
            curr_player = players[i][1]

            take = 0
            if curr_player >= max_score:
                # take this player
                take = curr_player + recurse3(i+1, curr_player)
            # skip this player
            skip = recurse3(i+1, max_score)

            best = max(take, skip)
            memo[(i, max_score)] = best
            return best
        
        def recurse4(curr: int, last: int) -> int:
            nonlocal n, players, memo
            if curr == n:
                return 0
            if last > -1 and memo[curr][last] != -1:
                return memo[curr][last]
            
            curr_player = players[curr][1]
            take_score = 0
            skip_score = 0

            # if there was no last player OR the new player has an equal or greater score to the last one
            if last == -1 or curr_player >= players[last][1]:
                # take this player
                take_score = curr_player + recurse4(curr+1, curr)
            # skip this player
            skip_score = recurse4(curr+1, last)

            best_score = max(take_score, skip_score)
            memo[curr][last] = best_score
            return best_score

        return recurse4(0, -1)
