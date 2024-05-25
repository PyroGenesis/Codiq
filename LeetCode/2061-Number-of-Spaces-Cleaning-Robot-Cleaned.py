from enum import Enum

class Direction(Enum):
    '''enum hused to indicate a direction'''
    EAST = 0
    SOUTH = 1
    WEST = 2
    NORTH = 3

    @classmethod
    def turn(cls, curr_direction: 'Direction'):
        '''gives a new direction, 90 degrees clockwise to given direction'''
        return cls((curr_direction.value + 1) % 4)

    @classmethod
    def move(cls, i, j, direction: 'Direction'):
        '''gives new indices after moving from the input indices in the direction given'''
        new_i, new_j = i, j
        if direction is cls.EAST:
            new_j += 1
        elif direction is cls.SOUTH:
            new_i += 1
        elif direction is cls.WEST:
            new_j -= 1
        else:
            new_i -= 1
        return new_i, new_j

'''
Skipped:
    BFS - Overcomplicated solution with the same time and space complexities as DFS
'''

class Solution:
    '''
    DFS Simulation
        Simulate the robots movement.
        We let the robot move, until we encounter an already seen combination of position and direction.
        If we only checked for position, we would miss the cases where the robot turns around and is able to clean more cells further ahead.

        Example:
                    ------>
        0 0 0 1 1     0 0 0 | 1 1
        1 1 0 1 1  => 1 1 0 | 1 1
        0 0 0 0 0     0 0 0 v 0 0
                    <------
                    ---------->

        We keep moving and turning, until we hit the same combination of position and direction. 
        This means that all reachable cells have been cleaned and so we return the number of cells cleaned.

        If m -> number of rows, n -> number of columns
        Time:  O(m*n)
        Space: O(m*n)
    '''
    def numberOfCleanRooms(self, room: list[list[int]]) -> int:
        m, n = len(room), len(room[0])
        visited = set()     # the set of visited (position and direction)
        cleaned = set()     # the set of visited positions only
        curr_pos, curr_dir = 0, Direction.EAST

        # continue until we encounter a visited position and direction
        # a visited position and direction would mean that we have already gone through all possible dirty cells
        while (curr_pos, curr_dir) not in visited:
            # clean current cell
            cleaned.add(curr_pos)
            # mark current position and direction as visited
            visited.add((curr_pos, curr_dir))

            # translate position to indices
            i, j = curr_pos // n, curr_pos % n
            # attempt to move in the current direction
            new_i, new_j = Direction.move(i, j, curr_dir)

            # if the move is invalid, turn instead
            if not (0 <= new_i < m) or not (0 <= new_j < n) or room[new_i][new_j] == 1:
                curr_dir = Direction.turn(curr_dir)
            else:
                # otherwise, update the position and loop
                curr_pos = new_i * n + new_j
        
        # return the number of cells cleaned
        return len(cleaned)
