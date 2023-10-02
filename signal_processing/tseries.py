import pandas as pd

class Signal:
    def __init__(self, fpath:str):
        df = pd.read_csv(fpath)
        df_tseries = df[['Time', 'signal']]
        df_tseries.set_index('Time', inplace=True)
        df_tseries['Trade'] = 0

        self.data = df_tseries
        