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
    # Wrapper around identify trend method allowing for parameter tuning
    process.identify_trend_grid(grid=np.linspace(0, 1.5, 100, endpoint=False), plot_grid=True)
    process._identify_trend(threshold=0.9, plot=True)
    plt.show(block=True)


if __name__ == "__main__":
    main()