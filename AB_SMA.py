#!/usr/bin/python3

import sys
import heapq

#TODO: the tree still needs to be implemented, but this can be done with one of two  

#ACTIONS: get preformed with a single function call to parameters
#functions dont return as Python passes value by obj ref 
#this handes the mod math so everything will go in a loop

class SMA:
    def __init__(self, max_nodes=200000):
        self.max_nodes = max_nodes
        self.nodes = {}
        self.queue = []

    def solve(self, start_node):
        start_key = tuple(start_node.normalizeBoard())

        #initialize start node then create queue
        self.nodes[start_key] = start_node
        heapq.heappush(self.queue, (start_node.f, start_node.heuristic, start_key))

        while self.queue:
            f, h, key = heapq.heappop(self.queue)
            
            # get node from key
            current = self.nodes.get(key)

            # with sma we end up removing keys so its possible current becomes none
            if current == None:
                continue

            # return current if it is solution
            if current.checker():
                return current

            # get successors
            successors = current.getSuccessors()
            for child in successors:
                child_key = tuple(child.normalizeBoard())

                # check memory
                if len(self.nodes) >= self.max_nodes:
                    self.prune_worst()

                # add child to nodes
                if child_key not in self.nodes:
                    self.nodes[child_key] = child
                    heapq.heappush(self.queue, (child.f, child.heuristic, child_key))
        
        return None

    def prune_worst(self):
        # if queue is empty return
        if not self.queue:
            return

        # sort queue
        self.queue.sort()

        # remove bottom 20% of nodes
        to_remove = self.queue[int(self.max_nodes*0.8):]
        self.queue = self.queue[:int(self.max_nodes*0.8)]

        for i, j, key in to_remove:
            if key in self.nodes:
                del self.nodes[key]

        heapq.heapify(self.queue)
    
    

class State:
    def __init__(self, board_state, shift_values, size):
        #inited both and can be shuffeled 
        self.board_state = list(map(int, board_state))
        self.shift_values = list(map(int, shift_values))
        self.cost=0
        self.size=int(size)
        self.heuristic = self.getHeuristic()
        self.f = self.cost + self.heuristic
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
        new.heuristic = self.heuristic
        new.f = self.f
        new.parent = self.parent
        return new

    #gets the index of null
    def getNullIndex(self):
        return self.board_state.index(0)

    # gets a normalized board
    def normalizeBoard(self):
        null = self.getNullIndex()
        return self.board_state[null:] + self.board_state[:null]

    # heuristic finds how far a tile is from its desired indicies and adds
    # the estimated number of moves to reach those indices.
    # it is calculated by dividing the distance by the largest shift value
    def getHeuristic(self):
        normalized = self.normalizeBoard()
        n = int((self.size - 1) ** 0.5)
        h = 0
        max_shift = max(self.shift_values)

        for i in range(1, self.size):
            tile = normalized[i] # current tile
            start = ((tile - 1) * n) + 1    # start of valid indicies
            end = tile * n                  # end of valid indicies

            # continue if alread in valid indicies
            if (i >= start) and (i <= end):
                continue
            start_dist = min((i - start) % self.size, (start - i) % self.size)
            end_dist = min((i - end) % self.size, (end - i) % self.size)
            best_dist = min(start_dist, end_dist)
            h += -(best_dist//-max_shift) # -(a//-b) is ceiling integer division

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
        child.f = max(self.f, child.cost+child.heuristic)
        successors.append(child)

        # create child 2
        child = self._copy()
        child.parent=self
        child.cost += 1
        child.shiftRight()
        child.heuristic=child.getHeuristic()
        child.f = max(self.f, child.cost+child.heuristic)
        successors.append(child)

        # check if shift value is 1
        if (self.getShiftValue() != 1):
            # create child 3
            child = self._copy()
            child.parent=self
            child.cost += 1
            child.leftShiftByValue()
            child.heuristic=child.getHeuristic()
            child.f = max(self.f, child.cost+child.heuristic)
            successors.append(child)

            # create child 4
            child = self._copy()
            child.parent=self
            child.cost += 1
            child.rightShiftByValue()
            child.heuristic=child.getHeuristic()
            child.f = max(self.f, child.cost+child.heuristic)
            successors.append(child)
        
        # sort successors by f
        successors.sort(key=lambda s: s.f)
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
    
    # Solve and Print
    SMAsolver = SMA() # SMA* solver
    solution = SMAsolver.solve(start_node)
    
    if solution:
        print("Solution is")
        path = solution.getPath()
        for node in path:
            print(node)
    else:
        print("No solution")