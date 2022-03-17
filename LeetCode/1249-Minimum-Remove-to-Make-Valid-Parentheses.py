class Solution:
    '''
    Stack / Greedy (Optimal)
        Consider a string with paranthesis that you are iterating on
        Let's say you keep a balance which starts with 0 and increments on every '(' and decrements on every ')'
        What happens if there are more ')' than '(' (or more ')' seen before '(')?
            The balance will go -ve
            If the balance goes -ve at any point, the string will not be valid
            Therefore, we need to remove all ')' that occur when the balance is already 0
            It would be impossible to remove less ')', because there are not enough '(' before them
        But we are not done yet
        If there are more '(' than ')' in the string, the balance will turn out +ve in the end
        We need to remove some '(' so that the balance becomes 0 at the end and the string is valid
        But we cannot remove '(' randomly, because we might remove a '(' that matches a ')'
            Therefore, we use a stack to store unmatched '(' indices which we erase after matching all ')'
    
        We keep a stack of indices of unmatched open brackets
        When we encounter a close bracket, there are 2 cases:
            Case 1: We do have at least 1 unmatched open bracket
                    Therefore, we match the close bracket with the last open bracket and remove the open bracket
                        from the stack
            Case 2: We do not have any unmatched open brackets
                    If we the stack is empty, either we exhausted all our prev open brackets OR we never encountered any
                    In either case, this close bracket can never be valid so we simply erase it
        After we are done iterating over the initial string, we might have unmatched open brackets left in stack.
        These can never be matched and are in excess, so we erase all of them
        The remaining string will be the string with the min number of paranthesis removed
        
        Implemenation Note:
            Its better to pick a arr to represent the string here while editing since it will be mutable
            Otherwise we will end up storing all partial immutable strings in memory
            
        Time:  O(n)
        Space: O(n)
    '''
    def minRemoveToMakeValid(self, s: str) -> str:
        stack = []      # stack of indices containing unmatched brackets
        s_arr = list(s) # the string as a list
                        # this is done because strings are immutable and it's better to edit lists
        
        # Go through each char of string
        for i, ch in enumerate(s_arr):
            if ch == '(':
                # if the char is an open bracket, add it to the stack
                stack.append(i)
            elif ch == ')':
                # if the char is a closed bracket
                if stack:
                    # we try to match with the last unmatched open bracket we have in the stack
                    stack.pop()
                else:
                    # otherwise, we clear out this close bracket since there is no open bracket to match to
                    s_arr[i] = ''
        
        # there might be unmatched open brackets left in the string
        # since there are no close brackets left to match to, we clear them out
        for i in stack:
            s_arr[i] = ''
        
        # we create our string by joining the array and return
        return ''.join(s_arr)
