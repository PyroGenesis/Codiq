from typing import List
from collections import defaultdict, deque

class Solution:
    '''
    Skipped: DFS solutions
        They do not have any lower time or space complexity than BFS but are more complicated to implement
        My opinion is that they don't really fit into the problem defined very well
            Which is to know the number of levels
    '''

    '''
    BFS (Kahn's Algorithm)
        The idea is to run a BFS while keeping a queue of the courses that can be immediately taken
        When each course is taken, it frees up its dependants which may be added to the queue to be taken next semester
        This is done effectively by 
        - keeping an prereq_count for every course that tells you whether a course has satisfied all its prereqs, and
        - a dependent count to effectively reduce the prereq_count of the dependants when the parent course is taken

        If a cyclic dependency is present, some courses will be never be added to queue and will still have dependants
        So we can prepare for it by deleting the dependant list for a course when its taken, and
            seeing if the depandant list is empty at the end
        
        v -> courses and e -> course to prereq relationships
        Time:  O(v+e)
            O(e) for iterating over relations
            O(v) for initially filling up queue
            O(v+e) for BFS because we visit every node and edge once
        Space: O(v+e)
            dependants is the biggest data structure with all courses and relations = O(v+e)
    '''
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        # The edges coming in to a node
        # Represents the number of prerequisites for a course
        prereq_count = [0]*(n+1)
        # represents the prerequisite to dependant course relationship
        # every course in this dict points to the list of courses it enables
        dependants = defaultdict(list)
        
        # fill the indegree and dependant data structures
        for a, b in relations:
            dependants[a].append(b)
            prereq_count[b] += 1
        
        # These are the courses that are available to take. 
        # They either don't have any prereqs or have all their prereqs satisfied
        available_courses = deque()
        for course in range(1, n+1):
            if prereq_count[course] == 0:
                available_courses.append(course)
        
        semester = 0
        while available_courses:
            # inc semester
            semester += 1

            # take all courses that are available
            courses_this_sem = len(available_courses)
            for _ in range(courses_this_sem):
                course = available_courses.popleft()
                for next_course in dependants[course]:
                    # reduce prereqs of all dependent courses when taking this course
                    prereq_count[next_course] -= 1
                    # if a course ends up satisfying all prereqs due to this reduction
                    # add it to the queue to be taken next semester
                    if prereq_count[next_course] == 0:
                        available_courses.append(next_course)
                # delete the dependant list for this course
                del dependants[course]
        
        # if there are any courses left over at this stage, it is a cyclic dependency
        # otherwise simply return the semesters we spent
        return semester if not dependants else -1
