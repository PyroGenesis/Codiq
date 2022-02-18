class Solution:
    
    '''
    Greedy, Optimal
        We greedily pick up digits from the left side list.
        If our new digit is smaller than the last digit picked, then we discard last picked digits until either:
        1. We run out of digits to discard
        2. We cannot discard anymore digits (k exceeded)
        3. last picked digit is now smaller than new pick
        Now after checking the last picks, if our new pick will not lead to a leading 0, we add it to our list
        
        At the end if we did not cross our digit removal limit, k, we will be left with a monotonic increasing sequence
        So we simply remove the rest of possible digits from the right end 
    
        Why does this not make things worse / Why is this optimal?
        Because removing num[i] and replacing it with num[i+x] gives far more benefit than:
        * The benefit wasted if any large digit was not removed in the latter part of the num
        * The benefit gained if any other digit was removed in the latter part of the num
        
        Proof:
          Eg: 2198789879, k=1
          Here you can see that removing the 2 will give us a num   1xxxxxxxx OR num < 200000000
          However removing any other digit will give us a num       2xxxxxxxx OR 200000000 < num < 300000000
            You can see that removing 2 and replacing it by 1 gives us the optimal result
            
          Eg2: 13589, k=1
          This is a monotonic increasing sequence and our greedy picks will pick every digit
          At the end, we will see that the only optimal digit to remove is the 9 at the end
        
        Time:  O(n)
        Space: O(n)
    '''
    def removeKdigits(self, num: str, k: int) -> str:
        n = len(num)
        
        # sanity check - if we have permission to remove all digits, ans = 0
        if k >= n:
            return "0"
        
        # the result, in the form of an array (to avoid string dups) of characters of digits
        # this will be also used as a working stack as a later low digit might be so good that we would
        #   get a better result if we removing multiple digits before it
        res_arr = []
        
        # We iterate from left to right as removals on the left of the number are far more valuable
        #   than removals on the right side if the number
        for i in range(n):
            # We can only remove digits based on 3 conditions:
            # 1. If we are allowed to (OR if we haven't already removed enough digits) [k > 0]
            # 2. Current ans has digits to remove [res_arr]
            # 3. The new digit, when moved into the prev order of magnitude, will result in a smaller number
            #    This means that the current solution's last digit can be replaced by this smaller digit 
            #      to get a smaller number overall
            while k > 0 and res_arr and res_arr[-1] > num[i]:
                res_arr.pop()
                k -= 1
            
            if len(res_arr) == 0 and num[i] == '0':
                # handling leading zeroes - just skip them
                continue
            else:
                # add the current digit to the resultant number
                res_arr.append(num[i])
        
        # After the loop, we have (tried to) remove all the intermediate digits which would make the answer smaller
        # Now, we are left with a list of digits in a monotonic increasing sequence
        # Removing any digit in the middle will only make significant digits bigger
        # If we want to remove more digits, the only solution is to remove digits from the end greedily
        # Only do this if we are allowed to remove more digits, i.e., k > 0
        # This is the quick but slightly less mem efficient way of doing this (insignificant)
        if k > 0:
            res_arr = res_arr[:-k]
        
        # This is the longer way to remove those digits from the end
        # for j in range(k):
        #     # Mistake 2 - Make sure you do not try to remove more digits than exist in the answer
        #     if not res_arr: break
        #     res_arr.pop()
        
        # Mistake 1 - k could be large enough so that with the help of leading 0s it is able to remove all significant digits
        #             So do check if the result is empty and return "0" appropriately
        return ''.join(res_arr) if res_arr else "0"
    
    '''
    Skipped:
        REGEX soln - Very inefficient
    '''
