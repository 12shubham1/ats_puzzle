from ant import Ant
from board import Board
from distfit import distfit
import numpy as np
from scipy import stats

class AntSimulation:

    def __init__(self, verbose:bool, diagonal:bool=False, backtrack:bool=False, objective='SAME', name=None):
        self.name = name
        self.verbose = verbose
        self.objective = objective
        self.diagonal = diagonal
        self.backtrack = backtrack
    
    def run(self, N=None):
        N = N if N is not None else 1
        results = []
        for i in range(N):
            res = self._run_one()
            if self.verbose:
                print(f"Game: {i} -> {res}")
            if res != -1:
                results.append(res)
            else:
                print(f"Game: {i} no result")
        
        return ResultsAnalyzer(results, self.name)
    
    def _run_one(self):

        # inst
        self.board = Board(
            Ant(), 
            Ant(is_ant_1=False), 
            backtrack=self.backtrack, 
            diagonal=self.diagonal, 
            objective=self.objective,
            verbose=self.verbose
        )

        num_turns = 0
        while True:
            num_turns+= 1
            if self.verbose:
                print(num_turns)
            # Returns true if game complete
            if self.board.next():
                break
            elif num_turns > 5_000:
                num_turns = -1
                break

        
        return num_turns
    
class ResultsAnalyzer:

    def __init__(self, data, name):
        self.data = data
        self.name = name

    def identify_distribution(self, plot:bool=False):
        dist = distfit()
        dist.fit_transform(np.array(self.data))
        distribution = eval(f'stats.{dist.model["name"]}(*dist.model["params"])')
        if plot:
            dist.plot(title=self.name)
        self.output_data = {
            'model_name': dist.model['name'], 'expectation': dist.model['model'].expect(), 
            'std': dist.model['model'].std(), 'distribution_fitted': distribution,
            'kstest_fitted': stats.kstest(self.data, distribution.cdf)
        }
    
    def force_log_norm(self):

        # Lognorm fit
        shape, loc, scale = stats.lognorm.fit(self.data)
        _dist = stats.lognorm(shape, loc, scale)
        self.output_data['lognorm_kstest'] = stats.kstest(self.data, _dist.cdf)
        self.output_data['norm_mu'] = np.log(scale)
        self.output_data['norm_std'] = shape
        self.output_data['lognorm_expect'] = _dist.expect()