import pandas as pd

class Trades:
    def __init__(self, fpath:str):
        df = pd.read_csv(fpath)
        df_trades = df[['Trade Timestamps']]
        df_trades.dropna(inplace=True)
        df_trades['Trade'] = 1
        df_trades.rename(columns={'Trade Timestamps': 'Time'}, inplace=True)
        df_trades.set_index('Time', inplace=True)

        self.data = df_trades