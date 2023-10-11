from tseries import Signal
from trades import Trades
from processing import Processor
import os, sys
import numpy as np
import matplotlib.pyplot as plt

def main():
    
    # Reading in data
    fpath = os.path.join(sys.path[0], "Test Data.csv")
    sig = Signal(fpath)
    trd = Trades(fpath)

    # Instantiate signal processor
    process = Processor(sig, trd)
    process.align_signal_trades()
    process.profile_signal(plot=True)
    process.profile_trade_to_signal(plot=True)

    # Wrapper around identify trend method allowing for parameter tuning
    process.identify_trend_grid(grid=np.linspace(0.5, 1.5, 100, endpoint=False), plot_grid=True)
    process._identify_trend(threshold=0.5, plot=True)
    process._identify_trend(threshold=1, plot=True)
    process._identify_trend(threshold=1.5, plot=True)
    plt.show(block=True)


if __name__ == "__main__":
    main()