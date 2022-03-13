class Solution:
    '''
    Stack
        A very simple algorithm
        Keep a stack of open parans as you iterate over the brackets
        When you reach a closing bracket, pop from the stack and try to match them uo
        
        There are 3 ways to fail the validity here:
        1. Getting a closing bracket that does not match last opening bracket
        2. Getting a closing bracket but with no opening brackets left in stack (IMP! Don't forget)
        3. Having the stack not be empty at the end (exira opening brackets)
    '''
    def isValid(self, s: str) -> bool:
        # dictionary which maps open brackets -> close brackets
        # very useful since it can not only match the opening and closing brackets, but
        #   it can also serve as a check whether a bracket is opening or closing
        bracket_pairs = {
            '(': ')',
            '[': ']',
            '{': '}'
        }
        
        # syntactic sugar to tell whether a bracket is a open bracket
        def isOpenParan(b):
            nonlocal bracket_pairs
            return b in bracket_pairs
        
        # syntactic sugar to get the closing bracket of an open bracket
        def getClosingParan(b):
            nonlocal bracket_pairs
            return bracket_pairs[b]
            
        # the stack that stores the unpaired open brackets (in order)
        stack = []
        
        # go through bracket string
        for bracket in s:
            if isOpenParan(bracket):
                # if it is an open bracket, just add it to the stack
                stack.append(bracket)
            else:
                # if it is a closing bracket ...
                
                # if no open brackets left unpaired, fail
                if not stack: return False
                # pop out last open bracket and try to pair with it, else fail
                open_bracket = stack.pop()
                if bracket != getClosingParan(open_bracket): return False
        
        # if there are unpaired brackets left over, fail
        return not stack
