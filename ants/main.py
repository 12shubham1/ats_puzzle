from simulation import AntSimulation
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import time
import config as c
import pandas as pd
import random
random.seed(1)


def run():
    start = time.perf_counter()

    tests = {
        'Adjacent, Backtrack, Meet': (False, True, 'SAME'),
        'Adjacent, No Backtrack, Meet': (False, False, 'SAME'),
        'Diagonal, Backtrack, Meet': (True, True, 'SAME'),
        'Diagonal, No Backtrack, Meet': (True, False, 'SAME'),
        #'Adjacent, Backtrack, Cross': (False, True, 'CROSS'),
        #'Adjacent, No Backtrack, Cross': (False, False, 'CROSS'),
        'Diagonal, Backtrack, Cross': (True, True, 'CROSS'),
        'Diagonal, No Backtrack, Cross': (True, False, 'CROSS'),     
    } 

    all_results = []
    for k, v in tests.items():
        print(f'---------------- {k} ------------------')
        results = AntSimulation(verbose=False, backtrack=v[1], diagonal=v[0], objective=v[2], name=k).run(c.N)
        results.identify_distribution(plot=False)
        results.force_log_norm()
        all_results.append(results)
    
    log_norms = show_log_norm_fits(all_results)      
    compare_log_norm(log_norms)

    df = pd.DataFrame({x.name:x.output_data  for x in all_results}).T
    df['expectation'] = df['expectation'].astype(float)
    df['norm_mu'] = df['norm_mu'].astype(float)
    df['lognorm_expect'] = df['lognorm_expect'].astype(float)
    cols_to_keep = ['model_name', 'expectation', 'kstest_fitted', 'lognorm_kstest', 'lognorm_expect']

    result = df[cols_to_keep]
    result['Time (fit model)'] = (result['expectation']*10).round(2)
    result['Time (log norm)'] = (result['lognorm_expect']*10).round(2)
    print(result)
        
    end = time.perf_counter()
    print(f'Time taken: {end-start} seconds')
    plt.show(block=True)


def show_log_norm_fits(all_results):

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
        

def compare_log_norm(log_norms):
    
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
    

if __name__ == '__main__':
    run()