from tseries import Signal
from trades import Trades
import pandas as pd
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

class Processor:
    def __init__(self, signal: Signal, trades: Trades):
        self.signal = signal
        self.trades = trades
    
    def align_signal_trades(self):
        res = pd.concat([self.signal.data, self.trades.data], ignore_index=False)
        res = res.sort_index()
        res.fillna(method='ffill', inplace=True)

        self.combined = res
    
    def _identify_trend(self, threshold: float, plot:bool=False) -> Tuple[pd.DataFrame, pd.DataFrame]:

        # Create copy (as df is mutable) to avoid side effects
        res = self.combined.copy()
        # Calculate rolling difference on the index (timestamps)
        res.loc[res.index[1:], 'time_same'] = np.diff(res.index)
        # when the signal is constant for less than the threshold (and its not a trade row) -> classify as trade
        mask = (res['time_same'] < threshold) & (res['Trade'] != 1.0)
        res.loc[mask, 'predict'] = 1
        # Shift by 1 to avoid the trade row directly
        res['predict'] = res['predict'].shift(-1)
        res.fillna(0, inplace=True)

        # Check where we hit and don't hit
        missed = (res['Trade'] == 1.0) & (res['predict'] == 0.0)
        incorrect = (res['Trade'] == 0.0) & (res['predict'] == 1.0)
        missing = res[missed]
        wrong = res[incorrect]

        if plot:
            fig, ax = plt.subplots()
            ax.step(res.index, res.signal, where='post')
            # Plotting all trades correctly caught
            correct = (res['Trade'] == res['predict']) & (res['Trade'] == 1.0)
            ax.scatter(res[correct].index, res[correct].signal, c='lime', label=f'Correct: {100-round(100*len(missing)/len(self.trades.data), 2)}%')
            ax.scatter(res[missed].index, res[missed].signal, c='r', label=f'Missing: {round(100*len(missing)/len(self.trades.data), 2)}%')
            ax.scatter(res[incorrect].index, res[incorrect].signal, c='k', label=f'Wrong: {round(100*len(wrong)/len(self.trades.data), 2)}%')
            ax.set_xlabel('Timestamp (s)')
            ax.set_ylabel('Signal')
            ax.legend()
            fig.suptitle(f'Trade Identification stats -> Signal constant < {round(threshold,2)}s')

        return missing, wrong
    
    def identify_trend_grid(self, grid:NDArray=np.linspace(0, 10), plot_grid:bool=False):
        missing = {}
        wrong = {}
        for i in grid:
            print(f'Running test for {round(i, 2)}s')
            # Setting plot to false otherwise risk of too many graphs
            m, w = self._identify_trend(i, False)
            missing[i] = 100*len(m)/len(self.trades.data)
            wrong[i] = 100*len(w)/len(self.trades.data)

        if plot_grid:
            fig, ax = plt.subplots()
            ax.plot(missing.keys(), missing.values(), c='r', label='Missed')
            ax.plot(wrong.keys(), wrong.values(), c='k', label='Wrong')
            ax.set_xlabel('Signal Constant Time (s)')
            ax.set_ylabel('Percent of Correct Trades')
            ax.legend()
            fig.suptitle('Signal constant time tuning')