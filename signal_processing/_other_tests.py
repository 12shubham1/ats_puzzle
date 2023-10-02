import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import numpy as np
import scipy 
import bisect


# Reading data in
fpath = os.path.join(sys.path[0], 'Test Data.csv')
df = pd.read_csv(fpath)
df_tseries = df[['Time', 'signal']]
df_tseries.set_index('Time', inplace=True)
df_tseries['Trade'] = 0

df_trades = df[['Trade Timestamps']]
df_trades.dropna(inplace=True)
df_trades['Trade'] = 1
df_trades.rename(columns={'Trade Timestamps': 'Time'}, inplace=True)
df_trades.set_index('Time', inplace=True)

## ========== assign trade to signal ====================================
res = pd.concat([df_tseries, df_trades], ignore_index=False)
res = res.sort_index()
res.fillna(method='ffill', inplace=True)
fig, ax = plt.subplots()

ax.step(res.index, res.signal, where='post')
mask = res['Trade'] == 1
ax.scatter(res[mask].index, res[mask].signal, c='r')

## ========== Rolling diff - UNSUCCESFUL ====================================
## Calculate percentage change from prev
#df_tseries['diff'] = df_tseries['signal'].rolling(2).apply(lambda x: (x.iloc[1] - x.iloc[0]))
## Calculate average time between trades
#avg_trade = df_trades.reset_index()['Time'].rolling(2).apply(lambda x: x.iloc[1]-x.iloc[0])
#avg_trade = avg_trade.to_frame()
#avg_trade.dropna(inplace=True)
## Removing outliers
#avg_trade = avg_trade[(np.abs(scipy.stats.zscore(avg_trade['Time'])) < 3)]
#avg = avg_trade.mean().iloc[0]
#
#def my_method(df_tseries, threshold, avg=0.5):
#    trade_mask = df_tseries['diff'] > threshold
#    ts = df_tseries[trade_mask]
#    if ts.empty:
#        return 0
#    ts['predict'] = 1
#
#    def is_close(x):
#        _min, _max = max(0, x.name - avg/2), x.name + avg/2
#        mask = (df_trades.index >= _min) & (df_trades.index <= _max)
#        return 1 if df_trades.loc[mask, 'Trade'].max() > 0.5 else -1
#
#    # Check for each prediction, if there is a trade within +- (avg time/2)
#    ts['Close'] = ts.apply(is_close, axis=1)
#
#    return 100*(ts['Close'].sum()/ len(df_trades))
#
#all_results = []
#for threshold in np.linspace(0, 1, 20):
#    print(threshold)
#    result = my_method(df_tseries, threshold)
#    all_results.append(result)
#
#fig, ax = plt.subplots()
#ax.plot(np.linspace(0, 1, 20), all_results)
#plt.show()
#print(1)



## ========== FOURIER - no success ====================================
## Trying to apply a fourier transform based filter
#x,y = df_tseries.index.values, df_tseries.signal.values
#
## Applying fft
#resampled = scipy.signal.resample(y, len(y))
#ybal = resampled - np.mean(resampled)
#x_new = np.linspace(min(x), max(x), len(ybal))
#
#sampling_rate = x_new[1]-x_new[0]
#N = len(ybal)
#
#fourier = scipy.fft.rfft(ybal)
##plt.plot(rfftfreq(N, d=1/sampling_rate), 2*np.abs(rfft(signal))/N)
#frequency_axis = scipy.fft.rfftfreq(N, d=1.0/sampling_rate)
#norm_amplitude = 2*np.abs(fourier)/N
#
##fig, ax = plt.subplots()
##ax.plot(frequency_axis, norm_amplitude)
##plt.show()
#
#mask = (norm_amplitude < 0.008)
#norm_amplitude[mask] = 0
#
#filtered = scipy.fft.ifft(norm_amplitude)
#fig, ax = plt.subplots()
#ax.plot(x_new, filtered)
#plt.show()
#
## ========== FOURIER - no success ====================================


