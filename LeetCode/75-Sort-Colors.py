from typing import List
from collections import Counter

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        self.sortColorsOnePass(nums)
    
    '''
    Follow-up: Do it in one pass

    3 Pointer / Dijkstra solution
        The idea is to use pointers and swaps to maintain the boundary between 0s, 1s and 2s
            One pointer will go through the numbers (curr)
            One pointer will be at the boundary between 0s and 1s
                This boundary will expand (increment) when curr encounters a 0 and swaps it back
            One pointer will be at the boundary between 1s and 2s
                This boundary will expand (decrement) when curr encounters a 2 and swaps it forward
        This way we accumulate the colors in the correct places in a single pass

        One optimization we can add is an early exit once curr is past the boundary between 1s and 2s
            This is because anything beyond that boundary is guaranteed to be 2 and need not be checked
        
        Time: O(n) [one pass]
            Iterating curr to 0 to boundary_2: O(n)
        Space: O(1)
            3 pointers: O(3)
    '''
    def sortColorsOnePass(self, nums: List[int]) -> None:
        after_last_0, before_first_2 = 0, len(nums)-1
        curr = 0

        # this condition has to be <= instead of <
        # because the num at before_first_2 is likely not a 2 and still needs to be processed (if 0)
        while curr <= before_first_2:
            if nums[curr] == 2:
                # put the 2 at before_first_2
                nums[curr], nums[before_first_2] = nums[before_first_2], nums[curr]
                # update before_first_2
                before_first_2 -= 1
                # we don't move curr here since we still need to process the num swapped in from before_first_2
                # Here, even though curr didn't move, before_first_2 was decremented, still reducing the loop count left by 1
                #   and maintaining single pass time complexity
            
            elif nums[curr] == 1:
                # 1s should lie >= after_last_0 and <= before_first_2
                # curr is in this range already
                # so this 1 is already at the right place
                curr += 1

            else:
                # put the 0 at after_last_0
                nums[curr], nums[after_last_0] = nums[after_last_0], nums[curr]
                # update after_last_0
                after_last_0 += 1
                
                # update curr
                # Why do we need to do this?
                # think of what num could be at after_last_0 (that ends up at curr)
                #   0? not possible since every 0 is swapped back before after_last_0
                #   1? possible
                #   2? not possible since every 2 is swapped forward to > curr (and > after_last_0)
                # the only possibility is 1
                # amd since we know a 1 encountered at curr is already in the correct position
                curr += 1


    '''
    Simple Map solution
        Count out the frequency of 0,1,2
        Use the map to overwrite all nums in the list

        Time: O(n) [two pass]
            Creating the map:   O(n)
            Overwriting nums:   O(n)
        Space: O(1)
            Map:                O(3)
    '''
    def sortColorsSimpleMap(self, nums: List[int]) -> None:
        # frequency of the colors 0,1,2
        color_freq = Counter(nums)

        # write out each color based on its count into nums
        idx = 0
        for color in range(0, 3):
            for _ in range(color_freq[color]):
                nums[idx] = color
                idx += 1
