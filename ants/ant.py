import random
import config as c

class Ant:
    def __init__(self, is_ant_1:bool=True):
        self.prev = None
        self.moveset = None
        self.backtrack = None
        self.diagonal = None

        # Defining start pos based on being ant 1 or 2
        if is_ant_1:
            self.pos = [0,0]
        else:
            self.pos = [c.BOARD,c.BOARD]
    
    def move(self):
        """
        Identifying new move and applying it while storing previous location
        """
        # Store the previous moves
        self.prev_prev = self.prev.copy() if self.prev is not None else None
        self.prev = self.pos.copy()

        # Identify the possible next moves and pick one
        moves = self._identify_move()
        curr_move = random.choice(list(moves))

        # Apply next move
        self.pos[0] += curr_move[0]
        self.pos[1] += curr_move[1]

    def _identify_move(self) -> set:
        """
        Identify all allowed moves based on ruleset
        """
        new_move = self.moveset.copy()
        state = 'ALL'
        # Calculate state of ant based on board position
        if self.pos == [0,0]:
            state = 'TOP_LEFT'
        elif self.pos == [0, c.BOARD]:
            state = 'TOP_RIGHT'
        elif self.pos == [c.BOARD, 0]:
            state = 'BOTTOM_LEFT'
        elif self.pos == [c.BOARD, c.BOARD]:
            state = 'BOTTOM_RIGHT'
        elif self.pos[0] == 0:
            state = 'TOP'
        elif self.pos[0] == c.BOARD:
            state = 'BOTTOM'
        elif self.pos[1] == 0:
            state = 'LEFT'
        elif self.pos[1] == c.BOARD:
            state = 'RIGHT'
        else:
            state = 'ALL'
        
        # If backtrack not permitted, calculate prev move inverse i.e. move required
        # to go back to previous square
        if not self.backtrack:
            if self.prev_prev is not None:
                prev_move = {self.prev_prev[0]-self.prev[0], self.prev_prev[1]-self.prev[1]}
            else:
                prev_move = set()
        else:
            prev_move = set()

        # Identify all possible moves in current step
        return new_move.difference(c.REMOVE_MAP[state].union(prev_move))
