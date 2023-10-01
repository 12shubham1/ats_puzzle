import random
import config as c

class Ant:
    def __init__(self, is_ant_1:bool=True):

        self.prev = None
        self.moveset = None
        self.backtrack = None
        self.diagonal = None

        if is_ant_1:
            self.pos = [0,0]
        else:
            self.pos = [c.BOARD,c.BOARD]
    
    def move(self):
        # Store the previous moves
        self.prev_prev = self.prev.copy() if self.prev is not None else None
        self.prev = self.pos.copy()

        # Identify the possible next moves and pick one
        moves = self._identify_move()
        curr_move = random.choice(list(moves))

        # Apply next move
        self.pos[0] += curr_move[0]
        self.pos[1] += curr_move[1]

    def _identify_move(self):
        new_move = self.moveset.copy()
        state = 'ALL'
        # If top_left
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
        
        if not self.backtrack:
            if self.prev_prev is not None:
                prev_move = {self.prev_prev[0]-self.prev[0], self.prev_prev[1]-self.prev[1]}
            else:
                prev_move = set()
        else:
            prev_move = set()

        return new_move.difference(c.REMOVE_MAP[state].union(prev_move))





    


