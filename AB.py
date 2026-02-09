import sys

#TODO: the tree still needs to be implemented, but this can be done with one of two  

#ACTIONS: get preformed with a single function call to parameters
#functions dont return as Python passes value by obj ref 
#this handes the mod math so everything will go in a loop
    

class State:
    def __init__(self, board_state, shift_values, size):
        #inited both and can be shuffeled 
        self.board_state = list(map(int, board_state))
        self.shift_values = list(map(int, shift_values))
        self.cost=0
        self.size=int(size)
        self.distanceMatrix = 0
        self.heuristic = 0
        self.parent=None

    # needed for checking membership in frontier
    def __eq__(self, other):
        if other is None or not isinstance(other, State):
            return False
        return self.board_state == other.board_state

    # needed to pass object in heapq
    def __lt__(self, other):
        return self.cost+self.heuristic < other.cost+other.heuristic
        
    # string method
    def __str__(self):
        return " ".join(map(str, self.board_state))
    
    # lightweight copy instead of deepcopy
    def _copy(self):
        new = State.__new__(State)
        new.board_state = self.board_state[:]  # only this needs copying (gets mutated)
        new.shift_values = self.shift_values    # shared ref, never mutated
        new.cost = self.cost
        new.size = self.size
        new.distanceMatrix = self.distanceMatrix
        new.heuristic = self.heuristic
        new.parent = self.parent
        return new

    #gets the index of null
    def getNullIndex(self):
        return self.board_state.index(0)

    # gets a normalized board
    def normalizeBoard(self):
        null = self.getNullIndex()
        return self.board_state[null:] + self.board_state[:null]

    # calculate matrix of distances from any given point, to every other point
    def getDistances(self):
        # initialize matrix
        matrix = [[float("inf") for _ in range(self.size)] for _ in range(self.size)]

        # assemble matrix
        for i in range(self.size):
            matrix[i][i] = 0
            queue = [(i, 0)]

            while queue:
                curr, dist = queue.pop(0)
                k = self.shift_values[curr]

                # find all possible moves
                moves = [(curr + 1) % self.size, (curr - 1) % self.size, (curr + k) % self.size, (curr - k) % self.size]

                for next_pos in moves:
                    # if matrix position is unassigned
                    if matrix[i][next_pos] == float("inf"):
                        # assign value and append to queue
                        matrix[i][next_pos] = dist + 1
                        queue.append((next_pos, dist + 1))
        
        self.distanceMatrix=matrix
        return

    # gets the minimum number of moves needed for each tile to move to a desired
    # position. returns sum
    def getHeuristic(self):
        normalized = self.normalizeBoard()
        n = int((self.size - 1) ** 0.5)
        h = 0

        # loop through tiles
        for i in range(1, self.size):
            tile = normalized[i]

            # find valid range for tile
            start = ((tile - 1) * n) + 1
            end = tile * n

            # find minimum from valid ranges to i
            # must find path from desired destination to current since 0 is the only tile that moves
            mindist = min(self.distanceMatrix[j][i] for j in range(start, end + 1))
            h += mindist

        return h


    
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
        temp = self.normalizeBoard()
        goal = sorted(temp)
        return temp == goal

    # gets children of given state
    def getSuccessors(self):
        successors=[]

        # create child 1
        child = self._copy()
        child.parent=self
        child.cost += 1
        child.shiftLeft()
        child.heuristic=child.getHeuristic()
        successors.append(child)

        # create child 2
        child = self._copy()
        child.parent=self
        child.cost += 1
        child.shiftRight()
        child.heuristic=child.getHeuristic()
        successors.append(child)

        # check if shift value is 1
        if (self.getShiftValue() != 1):
            # create child 3
            child = self._copy()
            child.parent=self
            child.cost += 1
            child.leftShiftByValue()
            child.heuristic=child.getHeuristic()
            successors.append(child)

            # create child 4
            child = self._copy()
            child.parent=self
            child.cost += 1
            child.rightShiftByValue()
            child.heuristic=child.getHeuristic()
            successors.append(child)
        
        # sort successors by heuristic
        successors.sort(key=lambda s: s.heuristic)
        return successors
        
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
    # solves puzzle 
    def solve_ida(self): 
        self.cost = 0 
        bound = self.heuristic
        while True: 
            visited = set() 
            result = ida_search(self, bound, visited) 
            if isinstance(result, State): 
                return result # solution found 
                
            if result == float('inf'): 
                return None # no solution 
                
            bound = result # increase threshold 
            

# IDA seach function 
def ida_search(node, bound, visited): 
    f = node.cost + node.heuristic
    if f > bound: 
        return f # return the minimum f that exceeded bound 
    
    if node.checker(): 
        return node # FOUND solution 
    
    min_excess = float('inf') 
    visited.add(tuple(node.normalizeBoard())) 
        
    for child in node.getSuccessors(): 
        state_key = tuple(child.normalizeBoard()) 
        if state_key in visited: 
            continue 
    
        result = ida_search(child, bound, visited) 
    
        if isinstance(result, State): 
            return result # solution found 
            
        min_excess = min(min_excess, result) 
    visited.remove(tuple(node.normalizeBoard())) 
        
    return min_excess

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

    # Initialize IDA State
    start_node = State(board_state, shift_values, n_disks)
    start_node.getDistances()
    start_node.getHeuristic()
    
    # Solve and Print
    solution = start_node.solve_ida() # IDA solver function
    
    if solution:
        print("Solution is")
        path = solution.getPath()
        for node in path:
            print(node)
    else:
        print("No solution")