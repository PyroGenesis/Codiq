class Solution:
    '''
    Stack
        Braindead solution and still optimal
            All alternatives are lesser
        Add chars to stack, but if '*' then pop instead
        Return string formed by chars in stack

        Time:  O(n)
        Space: O(n)
    '''
    def removeStars(self, s: str) -> str:
        stack = []
        for c in s:
            if c == '*':
                stack.pop()
            else:
                stack.append(c)
        
        return ''.join(stack)