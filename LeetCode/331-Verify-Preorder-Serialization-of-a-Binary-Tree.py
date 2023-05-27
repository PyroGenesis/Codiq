class Solution:
    def isValidSerialization(self, preorder: str) -> bool:
        return self.isValidSerializationStack(preorder)
        
    '''
        Initial, Almost-Optimal, Split Iteration
        Look at the question closely.
            If i give you a subset from start, will you be able to tell me easily if its valid
        You will quickly realize that the numbers don't matter
            There a given number of slots for any given tree structure
                and all of them must be filled, BUT
                there should be no more nodes than the number of slots
        How do we know how many slots to be filled?
        Look at the tree growth and you will find a pattern
            Initially, we have 1 slot available (for the root)
            For every new number node, we use up 1 slot but create 2 new ones
                Net change: +1
            For every null node, we use up 1 slot and create 0 new ones
                Net change: -1
        So if you keep track of this slot count, you can easily figure out if the traversal is valid
        NOTE: The traversal being preorder is basically useless
        
        Time:  O(n)
        Space: O(n)
    '''
    def isValidSerializationInitial(self, preorder: str) -> bool:
        # initially we have one empty slot to put the root in it
        slots = 1
        for node in preorder.split(','):
            # no empty slot to put the current node
            if slots == 0:
                return False
            
            if node == '#':
                # null node uses up a slot
                slots -= 1
            else:
                # number node creates a new slot
                slots += 1
        
        # we don't allow empty slots at the end
        return slots == 0
    
    '''
        Optimal, Character Iteration
        Similar logic as above, just skips the .split for char iteration
        This is because .split saves the split in a new list, costing us O(n) memory
        
        Time:  O(n)
        Space: O(n)
    '''
    def isValidSerializationCharIteration(self, preorder: str) -> bool:
        # initially we have one empty slot to put the root in it
        slots = 1
        # this boolean indicates whether current digit char indicates a new node (for multi-char numbers)
        new_symbol = True
        
        for ch in preorder:
            # if current char is a comma
            # get ready for next node and continue
            if ch == ',':
                new_symbol = True
                continue
                        
            # no empty slot to put the current node
            if slots == 0:
                return False
            
            if ch == '#':
                # null node uses up a slot
                slots -= 1
            elif new_symbol:
                # number node creates a new slot
                slots += 1
                # next letter is not a new node
                new_symbol = False
        
        # we don't allow empty slots at the end
        return slots == 0
    
    
    '''
        Stack
        Not better than initial, but interesting
    '''
    def isValidSerializationStack(self, preorder: str) -> bool:
        stack = []
        for node in preorder.split(","):            
            while stack and node == stack[-1] == "#":
                if len(stack) < 2:
                    return False                
                stack.pop()
                stack.pop()
            
            stack.append(node)
        
        return stack == ['#']