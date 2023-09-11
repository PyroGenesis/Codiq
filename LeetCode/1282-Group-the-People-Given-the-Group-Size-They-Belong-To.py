from typing import List
from collections import defaultdict

class Solution:
    '''
    Simple Greedy:
        The idea is simple, start by creating a hashmap from group_size to person arr
        As you iterate through people, add them to the right group using the hashmap
        When the group is full, put it in the ans arr and empty it in the hashmap

        Time:  O(n)
        Space: O(n)
    '''
    def groupThePeople(self, groupSizes: List[int]) -> List[List[int]]:
        n = len(groupSizes)

        # the final ans
        groups = []
        # intermediate groups
        incomplete_groups = defaultdict(list)

        for person in range(n):
            group_size = groupSizes[person]
            # add person to group
            incomplete_groups[group_size].append(person)

            # check if group is full
            if len(incomplete_groups[group_size]) == group_size:
                # add it to the final ans
                groups.append(incomplete_groups[group_size])
                # clear group from the hashmap
                # the reason why we do =[] and not .clear() is because the arr inside is a reference object
                incomplete_groups[group_size] = []
        
        # return the groups
        return groups
