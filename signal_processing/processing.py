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
    
    def profile_signal(self, plot:bool=True) -> pd.DataFrame:
        """
        Identify pattern in underlying signal (with trades removed from it) 
        """
        
        # Create a copy locally
        _temp = self.combined.copy()
        
        # Massage the data to identify all rolling time steps
        _temp.reset_index(inplace=True)
        _temp.at[1:, 'Diff'] = np.diff(_temp['Time'])
        _temp['Remove'] = _temp['Trade'].astype(bool)
        _temp['Remove'] = _temp['Remove'] | _temp['Remove'].shift(1) | _temp['Remove'].shift(-1)
        
        # Remove all trade + T-1, T+1 data points as these have been impacted by a
        # trade in some way
        _cleaned = _temp[_temp['Remove'] == False]

        # Plot the histogram
        if plot:
            fig, ax = plt.subplots()
            c, b = np.histogram(_cleaned['Diff'], len(_cleaned)//100)
            ax.stairs(c, b)
            ax.set_xlabel('Signal Step Time (s)')
            ax.set_ylabel('Frequency')
            fig.suptitle('Histogram of Signal Steps')

            fig, ax = plt.subplots()
            c, b = np.histogram(_cleaned['signal'], len(_cleaned)//100)
            ax.stairs(c, b)                                                  
            ax.set_xlabel('Signal Strength')
            ax.set_ylabel('Frequency')                                       
            fig.suptitle('Histogram of Signal Strength')

        return _cleaned
    
    def profile_trade_to_signal(self, plot:bool=True) -> pd.Series:
        """
        Plot distribution of time between trade arriving and signal changing
        """

        # Create a local copy
        _temp = self.combined.copy()
        _temp.reset_index(inplace=True)
        
        # Identify all cases where trade has happened
        _temp.at[1:, 'Diff'] = np.diff(_temp['Time'])
        # Shift trade by 1 to tag next point as trade completion
        _temp['Next'] = _temp['Trade'].shift(1)
        # Get difference of only those points tagged as trade completion
        mask = (_temp['Next'] == 1.0)
        _temp.loc[mask, 'Process_Time'] = _temp['Diff']
        pt = _temp['Process_Time']
        pt.dropna(ignore_index=True, inplace=True)

        # Plot
        if plot:
            fig, ax = plt.subplots()
            c, b = np.histogram(pt, len(pt)//100)
            ax.stairs(c, b)
            ax.set_xlabel('Processing Time (s)')
            ax.set_ylabel('Frequency')
            fig.suptitle('Histogram of Processing Time')

        return pt
        

    def align_signal_trades(self):
        """
        Concatenate the trade and signal data with a chronological index
        """
        res = pd.concat([self.signal.data, self.trades.data], ignore_index=False)
        res = res.sort_index()
        res.fillna(method='ffill', inplace=True)

        self.combined = res
    
    def _identify_trend(self, threshold: float, plot:bool=False) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Analyze signal and predict trades based on the following trend:
        - If signal is constant of 'threshold' or less, classify as a trade prediction
        Based on the above metric, calculate missing and wrong predictions (which are returned)
        """

        # Create copy (as df is mutable) to avoid side effects
        res = self.combined.copy()

        # Need to perform diff on non trades df
        self.signal.data.loc[self.signal.data.index[1:], 'time_same'] = np.diff(self.signal.data.index)
        # Apply calc on combined df
        res['time_same'] = self.signal.data['time_same']

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
        """
        Accessor to the _identify_grid method with additional support to tune the 'threshold' hyperparameter. 
        This method repeatedly calls _identify_trend across the grid specified. Results are stored in a dictionary
        and plotted.
        """

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