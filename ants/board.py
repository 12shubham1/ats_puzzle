import numpy as np
from ant import Ant
import config as c

class Board:

    def __init__(self, ant1:Ant, ant2:Ant, backtrack:bool=False, diagonal:bool=False, verbose:bool=True, objective:str='SAME'):
        self.ant1 = ant1
        self.ant2 = ant2
        self.base = np.zeros((c.BOARD,c.BOARD), dtype=int)
        self.verbose = verbose
        self.objective = objective
        self.diagonal = diagonal
        self.backtrack = backtrack
        self._apply_moveset_ants()
    
    def _apply_moveset_ants(self):
        allowed = c.MOVES.copy()
        # Only adjacent squares
        if not self.diagonal:
            for move in [c.UP_RIGHT, c.UP_LEFT, c.DOWN_LEFT, c.DOWN_RIGHT]:
                allowed.remove(move)

        self.ant1.moveset, self.ant2.moveset = allowed, allowed
        self.ant1.backtrack, self.ant2.backtrack = self.backtrack, self.backtrack

    def next(self):

        # Move ants
        self.ant1.move()
        self.ant2.move()

        if self.verbose:
            #if (self.ant1.pos == self.ant2.prev) or (self.ant2.pos == self.ant1.prev):
            print(f'Ant1: {self.ant1.pos} ({self.ant2.prev}) --- Ant2: {self.ant2.pos} ({self.ant1.prev})')

        return self.evaluate_state()
    
    def evaluate_state(self):
        if self.objective == 'SAME':
            return self.ant1.pos == self.ant2.pos
        elif self.objective == 'CROSS':
            return (self.ant1.pos == self.ant2.prev) and (self.ant2.pos == self.ant1.prev)
        
    