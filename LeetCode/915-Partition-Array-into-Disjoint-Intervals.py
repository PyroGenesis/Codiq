class Solution:
    '''
        Incomplete
    '''
    
    def partitionDisjoint(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        left_max = nums[0]
        global_max = nums[0]
        partition_length = 1
        
        for i in range(1, n):
            # every num on left has to be <= right, not < right (the example fooled me)
            if nums[i] < left_max:
                partition_length = i+1
                left_max = global_max
            else:
                global_max = max(global_max, nums[i])
                
        return partition_length
