class Solution:
    '''
    Optimal solution
    Keep an insertion pointer starting at 1 which is used to put in new non-duplicate nums
    An iterator it goes through the list from 1 to n-1 trying to get new unique nums
    If the current element (insert-1) and the next element (it) are the same,
        then we just keep on going till we find a different element
    If it finds a num != nums[insert - 1] (not the same as prev inserted num),
        that's a new num and insert consumes it before incrementing itself
        
    TIme:  O(n)
    Space: O(1)
    '''
    def removeDuplicates(self, nums: List[int]) -> int:
        # sanity check
        numslen = len(nums)
        if numslen < 2:
            return numslen
        
        # insertion pointer
        # it starts from 1 because 0th element is guaranteed to be unique
        insert = 1
        
        # iterator through nums list
        # Again, it starts from 1 because 0th element is guaranteed to be unique
        for it in range(1, numslen):
            # it curr iter num == prev inserted num [it is not unique]
            if nums[it] == nums[insert-1]:
                continue
            
            # curr num is a unique num
            nums[insert] = nums[it]
            insert += 1
        
        # the final insertion pointer index will be the length of the uniques
        return insert
