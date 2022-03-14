class Solution:
    '''
    Stack - Simple and optimal
        We use stack here to keep track of the path at each juncture
        We start by dividing the path using '/' which gives us all the parts
        
        Now we iterate through the parts in this way:
            1. If we encounter '' (because of double+ slashes) or '.' then do nothing and continue
            2. If meet .. element and stack is not empty, it means, that we need to go one level up, 
                so we just pop element from stack and forget about it.
            3. If we have any other element, we put it to the end of stack.
        In the end we reconstruct string from all element, using / at the start while joining them.

        Time:  O(n)
        Space: O(n)
    '''
    def simplifyPath(self, path: str) -> str:
        canonical_path = []
        
        for section in path.split('/'):
            if section == '' or section == '.':
                continue
            elif section == '..':
                if canonical_path: canonical_path.pop()
            else:
                canonical_path.append(section)
        
        return '/' + '/'.join(canonical_path)
