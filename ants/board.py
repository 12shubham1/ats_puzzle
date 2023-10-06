import numpy as np
from ant import Ant
import config as c
import time

class Board:
    def __init__(self, ant1:Ant, ant2:Ant, backtrack:bool=False, diagonal:bool=False, verbose:bool=True, objective:str='SAME'):
        # Creating board and ants associated
        self.ant1 = ant1
        self.ant2 = ant2
        self.base = np.zeros((c.BOARD+1,c.BOARD+1), dtype=int)
        self.verbose = verbose
        self.objective = objective
        self.diagonal = diagonal
        self.backtrack = backtrack
        # Identify, based on inputs, base allowed moveset for ants
        self._apply_moveset_ants()
    
    def _apply_moveset_ants(self):
        """
        Identify allowed moves for ants and apply to Ant instance
        """
        allowed = c.MOVES.copy()
        # Only adjacent squares
        if not self.diagonal:
            [allowed.remove(move) for move in [c.UP_RIGHT, c.UP_LEFT, c.DOWN_RIGHT, c.DOWN_LEFT]]

        # propogate outcome to ants
        self.ant1.moveset, self.ant2.moveset = allowed, allowed
        self.ant1.backtrack, self.ant2.backtrack = self.backtrack, self.backtrack

    def next(self) -> bool:
        """
        Call the next step in the simulation. At the end, it evaluates the board's 
        state and returns True is success criteria is met (else False).
        """

        # Move ants
        self.ant1.move()
        self.ant2.move()

        if self.verbose:
            #if (self.ant1.pos == self.ant2.prev) or (self.ant2.pos == self.ant1.prev):
            print(f'Ant1: {self.ant1.pos} ({self.ant2.prev}) --- Ant2: {self.ant2.pos} ({self.ant1.prev})')
            self.print_board()

        # Evaluate if success criteria met
        return self.evaluate_state()
    
    def print_board(self):
        """
        Useful in debugging where board and moves are printed 
        """
        blank = self.base.copy().astype('str')
        blank.fill('.')
        #blank[self.ant1.prev[0], self.ant1.prev[1]] = 'a'
        blank[self.ant1.pos[0], self.ant1.pos[1]] = 'A'
        #blank[self.ant2.prev[0], self.ant2.prev[1]] = 'b'
        blank[self.ant2.pos[0], self.ant2.pos[1]] = 'B'
        time.sleep(0.15)
        print(blank)
        
    
    def evaluate_state(self) -> bool:
        """
        Check if based on ants positions, the success criteria is met
        CROSS = (ant 1 previous = ant 2 current) & (ant 2 previous = ant 1 current)
        MEET = (ant 1 current = ant 2 current)
        """
        if self.objective == 'SAME':
            return self.ant1.pos == self.ant2.pos
        elif self.objective == 'CROSS':
            return (self.ant1.pos == self.ant2.prev) and (self.ant2.pos == self.ant1.prev)
        
    
