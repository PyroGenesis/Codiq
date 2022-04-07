from typing import List

# My import
import heapq as hq

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        return self.lastStoneWeightBucketSort(stones)
    
    '''
    Bucket Sort: Not a better soln than heap, just different
        Since the range of the stones' weights is not that large, we can use bucket sort
        Make buckets for weights from 1 to max weight
        Loop through all stones and increment the appropriate bucket
        Now loop backwards through the buckets, while keeping a variable for a stone in hand:
            If the bucket is empty, there is nothing we can do here
            While the bucket has something and we have something in hand
                Smash until either 
                 - the bucket gets empty OR
                 - the resultant stone in hand becomes lighter than the bucket
                   (in which case we remove that stone from hand and put it in its appropriate smaller bucket to be smashed later)
            If the bucket has something but we have nothing in hand, 
                Smash and eliminate all stones with each other in that bucket
                If there is a stone left untouched at the end, add that to your hand
        Whatever is left in hand at the end of this loop is the answer
        
        Time:  O(n + w), where w -> max_weight
                n for initializing buckets, max_weight for bucket loop
        Space: O(w) [for the buckets]
    '''
    def lastStoneWeightBucketSort(self, stones: List[int]) -> int:
        # the heaviest stone, used for initializing and iterating over the buckets
        biggest_stone = max(stones)
        # initialize the buckets
        # here we only care about weight 1 to biggest_stone
        buckets = [0]*(biggest_stone+1)
        
        # fill up the buckets with the right frequencies
        for stone in stones:
            buckets[stone] += 1
        
        # this is the stone in hand (always made to be the heaviest one at any point)
        curr_stone = 0
        
        # go over all the buckets from heaviest to lightest weights
        for bucket in range(biggest_stone, 0, -1):
            # if there are no stones with this weight, just skip it
            if not buckets[bucket]:
                continue
            
            # while we have a stone in hand, and there are stone(s) in the bucket
            #   keep smashing them
            while curr_stone and buckets[bucket]:
                # what's left after smashing
                diff = curr_stone - bucket
                if diff < bucket:
                    # if there is a stone lighter than current bucket (or nothing) left after smashing,
                    #   remove it from hand and add it to its appropriate bucket
                    # In case of nothing left, buckets[0] will be incremented but that's fine
                    #   because we will never reach it
                    buckets[diff] += 1
                    curr_stone = 0
                else:
                    # Otherwise, our stone in hand is ready to do some more smashing!
                    # Put the stone left, back in hand
                    curr_stone = diff
                # decrease the stone in the bucket since we used it
                buckets[bucket] -= 1
            
            # if we don't have a stone in hand
            if not curr_stone:
                # stones in current bucket will smash with themselves (because hand is empty)
                # this will lead to either 0 or 1 stone left
                # if there is a stone left after the bloodbath, add it to the hand
                if buckets[bucket] % 2 == 1:
                    curr_stone = bucket
                # bucket has been emptied
                buckets[bucket] = 0
        
        # return whatever stone is left in hand
        return curr_stone
                
    '''
    Heap solution:
        We keep a "max-heap" of all the current stones we have
        On every iteration, we take out two stones and smash them
            If there is anything left, we put it back in the heap
        In the end, we return if one stone (or nothing) remains
        
        Time:  O(nlogn)
                O(n) [making the heap] + O(n) [loop] * (logn [largest] + logn [2nd largest] + logn [put back remaining])
        Space: O(n)
                We do use the input itself as a heap, but since we destroy it, I'll still add it to the space complexity
    '''
    def lastStoneWeightHeap(self, stones: List[int]) -> int:
        # making all the stone weights negative so that we can use them in a min-heap as a max-heap
        for i in range(len(stones)):
            stones[i] *= -1
        
        # heapify the stones
        # Now, the heaviest stones will be at the front of the heap (with -ve weights)
        hq.heapify(stones)
        
        # simulate rocks smashing until either 1 stone is left or nothing is left
        while len(stones) > 1:
            # get the two heaviest stones (also fix -ve weights)
            largest, second_largest = -hq.heappop(stones), -hq.heappop(stones)
            
            # calculate what's left after smashing them
            remaining = largest - second_largest
            # if there is something left, add it back to the heap
            if remaining:
                hq.heappush(stones, -remaining)
        
        # return the last stone weight if available else 0
        return -stones[0] if stones else 0
