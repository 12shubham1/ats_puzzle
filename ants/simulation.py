from ant import Ant
from board import Board
from distfit import distfit
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from typing import Optional
import config as c


class ResultsAnalyzer:

    def __init__(self, data: list, name: str):
        self.data = data
        self.name = name

    def identify_distribution(self, plot:bool=False):
        """
        Use the 'distfit' module to identify the best distribution for the sample.
        The results are stored as an instance attribute in dictionary form in self.output_data
        """
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
        """
        Force a lognormal distribution on sample data to enable comparison
        """

        # Lognorm fit
        shape, loc, scale = stats.lognorm.fit(self.data)
        _dist = stats.lognorm(shape, loc, scale)
        # For fit distribution, calculate ks test score and underlying normal distribution
        self.output_data['lognorm_kstest'] = stats.kstest(self.data, _dist.cdf)
        self.output_data['norm_mu'] = np.log(scale)
        self.output_data['norm_std'] = shape
        self.output_data['lognorm_expect'] = _dist.expect()
    

    @staticmethod
    def show_log_norm_fits(all_results: list) -> list:
        """
        Plot all underlying normal distributions based on the fit lognormal distribution + compare
        to the histogram of the log of the sample
        """

        fig, axes = plt.subplots(2, 3, figsize=(9, 16))
        axes = axes.flatten()
        log_norms = []
        for idx, result in enumerate(all_results):

            # Plotting log data (raw) as histogram
            log_data = np.array(np.log(result.data))
            counts, bins = np.histogram(log_data, bins=int(c.N/100))
            ax = axes[idx]
            ax.stairs(counts, bins)

            # Plotting fit normal distribution on log of data
            ax2 = ax.twinx()
            xmin, xmax = ax.get_xlim()
            x = np.linspace(xmin, xmax, 100)
            mu, std = result.output_data['norm_mu'], result.output_data['norm_std']
            p = stats.norm.pdf(x, mu, std)
            ax2.plot(x, p, linewidth=2)
            ax2.set_ylim(0, ax2.get_ylim()[1])
            ax.set_title(f'{result.name} - ks score: {round(result.output_data["lognorm_kstest"][0], 2)}')

            log_norms.append((result.name, p, xmin, xmax, mu, std))
        
        fig.suptitle('Comparing fitted normal distributions to histogram of log(data)')
    
        return log_norms


    @staticmethod
    def compare_log_norm(log_norms):
        """
        Compare all underlying normal distributions on same chart
        """
        
        fig, ax = plt.subplots(figsize=(9, 16))
        ylims = -1
        for data in log_norms:
            test_name, fitted_points, xmin, xmax, mu, std = data

            x = np.linspace(xmin, xmax, 100)
            ax.plot(x, fitted_points, linewidth=2, label=f'{test_name} (mu={round(mu,2)},std={round(std,2)})')
            if ax.get_ylim()[1] > ylims:
                ylims = ax.get_ylim()[1]
                ax.set_ylim(0, ylims)
        
        ax.set_xlabel('Log of Data')
        fig.suptitle('Comparing fit normal distributions')
        
        plt.legend()

class AntSimulation:

    def __init__(self, verbose:bool, diagonal:bool=False, backtrack:bool=False, objective:str='SAME', name:Optional[str]=None):
        self.name = name
        self.verbose = verbose
        self.objective = objective
        self.diagonal = diagonal
        self.backtrack = backtrack
    
    def run(self, N:int=1) -> ResultsAnalyzer:
        """
        Simulation run accessor. Performs N similations and appends all results
        to a results list, which is used to instantiate a ResultsAnalyzer object.

        TODO: Parallelize the N runs
        """

        results = []
        # Run N simulations. TODO: Parallelize this in the future
        for i in range(N):
            res = self._run_one()
            if self.verbose:
                print(f"Game: {i} -> {res}")
            if res != -1:
                results.append(res)
            else:
                print(f"Game: {i} no result")
        
        return ResultsAnalyzer(results, self.name)
    
    def _run_one(self) -> int:
        """
        Main call to run simulation. The function approach is:
        1) Instantiate board and ants
        2) Call board.next() until success condition met OR 5000 turns exceeded
        3) Return result: -1 for no success or N
        """

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
    