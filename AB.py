from sys import argv
import copy
import heapq
import time

#TODO: the tree still needs to be implemented, but this can be done with one of two  

#ACTIONS: get preformed with a single function call to parameters
#functions dont return as Python passes value by obj ref 
#this handes the mod math so everything will go in a loop
    

class State:
    HEURISTIC_WEIGHT = 3 #to put more weight on the huristic 

    def __init__(self, board_state, shift_values, size):
        #inited both and can be shuffeled 
        self.board_state = list(map(int, board_state))
        self.shift_values = list(map(int, shift_values))
        self.cost=0
        self.size=int(size)
        self.inversions=self.getInversions()
        self.parent=None

    # lightweight copy instead of deepcopy
    def _copy(self):
        new = State.__new__(State)
        new.board_state = self.board_state[:]  # only this needs copying (gets mutated)
        new.shift_values = self.shift_values    # shared ref, never mutated
        new.cost = self.cost
        new.size = self.size
        new.inversions = self.inversions
        new.parent = self.parent
        return new

    # needed for checking membership in frontier
    def __eq__(self, other):
        if other is None or not isinstance(other, State):
            return False
        return self.board_state == other.board_state

    # needed to pass object in heapq
    def __lt__(self, other):
        return self.cost + self.inversions * State.HEURISTIC_WEIGHT < other.cost + other.inversions * State.HEURISTIC_WEIGHT
        
    #gets the index of null
    def getNullIndex(self):
        return self.board_state.index(0)

    # gets a normalized board
    def normalizeBoard(self):
        null = self.getNullIndex()
        return self.board_state[null:] + self.board_state[:null]
    
    # gets the number of inversions needed to reach goal state
    def getInversions(self):
        normalized = self.normalizeBoard()
        inversions=0
        for i in range(1, self.size):
            for j in range(i+1, self.size):
                if normalized[i] > normalized[j]:
                    inversions += 1
        return inversions
    
    #get the current shift value 
    def getShiftValue(self):
        return self.shift_values[self.getNullIndex()]
    
    #moved the empty space to the left 
    def shiftLeft(self):
        null= self.getNullIndex()
        self.board_state[null], self.board_state[(null-1)%self.size] = self.board_state[(null-1)%self.size], self.board_state[null]
     
    #moves the empty space to the right and time to to the left   
    def shiftRight(self):
        null= self.getNullIndex()
        self.board_state[null], self.board_state[(null+1)%self.size] = self.board_state[(null+1)%self.size], self.board_state[null]
        
    #swaps the space and tile to the right by the shift vaule of the space  
    def rightShiftByValue(self):
        null = self.getNullIndex()
        shiftValue = self.shift_values[null]
        self.board_state[null], self.board_state[(null+shiftValue)%self.size] = self.board_state[(null+shiftValue)%self.size], self.board_state[null]
        
        
     ##swaps the space and tile to the left by the shift vaule of the space
    def leftShiftByValue(self):
        null = self.getNullIndex()
        shiftValue= self.shift_values[null]
        self.board_state[null], self.board_state[(null-shiftValue)%self.size] = self.board_state[(null-shiftValue)%self.size], self.board_state[null]
    
    #checks the game state to see if it is a solution
    #return bool 
    def checker(self):
        null = self.getNullIndex()
        temp = self.normalizeBoard()
        goal = [0,1,1,1,2,2,2,3,3,3]
        if (self.size == 17):
            goal = [0,1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5]
            return temp == goal
        return temp == goal

    # gets children of given state
    def getSuccessors(self):
        successors=[]

        # create child 1
        child = self._copy()
        child.parent=self
        child.cost += 1
        child.shiftLeft()
        child.inversions=child.getInversions()
        successors.append(child)

        # create child 2
        child = self._copy()
        child.parent=self
        child.cost += 1
        child.shiftRight()
        child.inversions=child.getInversions()
        successors.append(child)

        # check if shift value is 1
        if (self.getShiftValue() != 1):
            # create child 3
            child = self._copy()
            child.parent=self
            child.cost += 1
            child.leftShiftByValue()
            child.inversions=child.getInversions()
            successors.append(child)

            # create child 4
            child = self._copy()
            child.parent=self
            child.cost += 1
            child.rightShiftByValue()
            child.inversions=child.getInversions()
            successors.append(child)

        return successors
    
    
    def check_transition(self, prev_state):
        """Return 'VALID' if this state is a valid move from prev_state, else 'INVALID'."""
        possible = [succ.board_state for succ in prev_state.getSuccessors()]
        if self.board_state in possible:
            return "VALID"
        else:
            return "INVALID"
        
        
    # gets path of states from initial to self
    def getPath(self):
        path=[]
        current=self
        while current != None:
            path.append(current)
            current = current.parent
        path.reverse()
        return path

    # solves puzzle
    def solve(self):
        # create frontier and closed
        # frontier is a priority queue using a heap
        frontier=[]
        closed=set()

        timeout_seconds = 20 * 60
        log_interval_seconds = 60
        start_time = time.monotonic()
        next_log_time = start_time + log_interval_seconds
        nodes_expanded = 0

        # push initial state to frontier
        # heapq selects for smallest first is smallest f, second is smallest h
        heapq.heappush(frontier, (self, self.inversions * State.HEURISTIC_WEIGHT))

        # start search
        while frontier:
            now = time.monotonic()
            if now - start_time >= timeout_seconds:
                return None, "timeout", now - start_time

            current, h = heapq.heappop(frontier)
            nodes_expanded += 1

            if now >= next_log_time:
                print(
                    "Elapsed: {:.1f}s | Expanded: {} | Frontier: {} | State: {}".format(
                        now - start_time, nodes_expanded, len(frontier), current.board_state
                    )
                )
                next_log_time = now + log_interval_seconds

            # check if current is solution
            if current.checker():
                return current, "solved", time.monotonic() - start_time

            # add current to closed
            closed.add(tuple(current.board_state))

            # add children to frontier if not in closed
            for child in current.getSuccessors():
                # Faster version:
                if tuple(child.board_state) not in closed:
                    heapq.heappush(frontier, (child, child.inversions * State.HEURISTIC_WEIGHT))
        
        # no solution
        return None, "no-solution", time.monotonic() - start_time

    def format_output(state_path):
        print("Solution is")  # Required header [cite: 52]
        for state in state_path:
            # Convert tuple/list of ints to space-separated strings
            print(" ".join(map(str, state.board_state)))
    
    def is_goal(board, n_disks):
        # Find the 0
        null_idx = board.index(0)
        # Rotate the board so 0 is at the front
        normalized = board[null_idx:] + board[:null_idx]
        # The '0' is at index 0. Check if the rest (1 to n_disks-1) is sorted
        just_disks = normalized[1:]

        return all(just_disks[i] <= just_disks[i+1] for i in range(len(just_disks)-1))

# if __name__ == "__main__":
#     shift_values=input().split()
#     board_state=input().split()
#     start = State(board_state, shift_values, argv[1])
#     solution = start.solve()
#     if (solution != None):
#         path = solution.getPath()
#         for node in path:
#             print(node.board_state)
#     else:
#         print("No solution")

if __name__ == "__main__":
    import sys
    import time
    from datetime import datetime
    # Get N from command line
    if len(sys.argv) < 2:
        print("Usage: python AB.py <number_of_disks>")
        sys.exit(1)
    n_disks = int(sys.argv[1])

    # Get the two lines of input - eroor checking to catch if sys doesnt exist
    try:
        # line 1: Shift values (from large disks) - make sure each number seperated by a space
        shift_input = sys.stdin.readline().split()
        # line 2: Board state (from small disks) - make sure each number seperated by a space
        board_input = sys.stdin.readline().split()
        
        # Convert strings to integers
        shift_values = [int(x) for x in shift_input]
        board_state = [int(x) for x in board_input]
        
    except EOFError:
        sys.exit(0)

    # Initialize A* State
    start_node = State(board_state, shift_values, n_disks)
    
    # Solve and Print
    wall_start = datetime.now()
    solution, reason, elapsed = start_node.solve() # A* solver function
    wall_end = datetime.now()
    
    if solution:
        print("Solution is")
        print("Wall clock start: {}".format(wall_start.isoformat(sep=" ", timespec="seconds")))
        print("Wall clock end: {}".format(wall_end.isoformat(sep=" ", timespec="seconds")))
        print("Elapsed seconds: {:.1f}".format(elapsed))
        path = solution.getPath()
        for i, node in enumerate(path):
            print(*(node.board_state), end=" ")
            print("START" if i == 0 else node.check_transition(path[i-1]))
    else:
        if reason == "timeout":
            print("Wall clock start: {}".format(wall_start.isoformat(sep=" ", timespec="seconds")))
            print("Wall clock end: {}".format(wall_end.isoformat(sep=" ", timespec="seconds")))
            print("Timeout after {:.1f} seconds".format(elapsed))
        else:
            print("No solution")