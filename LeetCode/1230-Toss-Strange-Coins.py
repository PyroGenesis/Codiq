from typing import List


class Solution:
    def probabilityOfHeads(self, prob: List[float], target: int) -> float:
        n = len(prob)
        # sanity check
        if target < 0 or target > n:
            return 0

        # target_prob[i] indicates the probability of getting i heads
        target_prob = [1]

        # toss coins and compute probability
        for head in prob:
            # probability of this coin landing on tails
            tail = 1 - head

            # initialize the new target_prob arr, starting with the probability of 0 heads
            # 0 heads is simply = prev probability of 0 heads * this coin also landing on tails
            new_target_prob = [target_prob[0] * tail]

            # compute the probabilities of intermediate targets
            for t in range(1, len(target_prob)):
                # this target can be reached with curr coin if either:
                #   we already have target-1 heads and this coin lands on heads
                #   we already have target heads and this coin lands on tails
                new_target_prob.append(target_prob[t-1] * head + target_prob[t] * tail)
            
            # finally add the probability of all heads
            # all heads is simply = prev probability of all heads * this coin also landing on heads
            new_target_prob.append(target_prob[-1] * head)

            # assign the new target probability array
            target_prob = new_target_prob
        
        # since we have compyted the probabilities of all possible targets,
        #   simply return the one we need
        return target_prob[target]
