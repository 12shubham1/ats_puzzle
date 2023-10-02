# RUN TIME PARAMS ===============================================
# Number of simulations per test case
N = 10_000

# Defining test cases
TESTS = {
        'Adjacent, Backtrack, Meet': (False, True, 'SAME'),
        'Adjacent, No Backtrack, Meet': (False, False, 'SAME'),
        'Diagonal, Backtrack, Meet': (True, True, 'SAME'),
        'Diagonal, No Backtrack, Meet': (True, False, 'SAME'),
        # THESE 2 TESTS ARE REMOVED AS THEY NEVER SUCCEED
        #'Adjacent, Backtrack, Cross': (False, True, 'CROSS'),
        #'Adjacent, No Backtrack, Cross': (False, False, 'CROSS'),
        'Diagonal, Backtrack, Cross': (True, True, 'CROSS'),
        'Diagonal, No Backtrack, Cross': (True, False, 'CROSS'),     
} 

# CHESSBOARD PARAMS ==============================================
# Board is NxN -> defined by this. Note: This is python index so 
# chessboard size = (board+1) x (board+1)
BOARD = 7

# Defining moves -> should be constants
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UP_RIGHT = (-1, 1)
UP_LEFT = (-1, -1)
DOWN_RIGHT = (1, 1)
DOWN_LEFT = (1, -1)

MOVES = {UP, DOWN, LEFT, RIGHT, UP_RIGHT, UP_LEFT, DOWN_RIGHT, DOWN_LEFT}

# Defining legal moves based on position
REMOVE_MAP = {
    'TOP': {UP, UP_RIGHT, UP_LEFT},
    'BOTTOM': {DOWN, DOWN_RIGHT, DOWN_LEFT},
    'LEFT': {LEFT, UP_LEFT, DOWN_LEFT},
    'RIGHT': {RIGHT, UP_RIGHT, DOWN_RIGHT},
    'TOP_LEFT': {UP, LEFT, UP_LEFT, DOWN_LEFT, UP_RIGHT},
    'TOP_RIGHT': {UP, RIGHT, UP_LEFT, DOWN_RIGHT, UP_RIGHT},
    'BOTTOM_LEFT': {DOWN, LEFT, DOWN_LEFT, UP_LEFT, DOWN_RIGHT},
    'BOTTOM_RIGHT': {DOWN, RIGHT, DOWN_LEFT, UP_RIGHT, DOWN_RIGHT},
    'ALL': set()
}
