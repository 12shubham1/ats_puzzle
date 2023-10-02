from simulation import AntSimulation, ResultsAnalyzer
import matplotlib.pyplot as plt
import time
import config as c
import pandas as pd

# Uncomment for replicating results
#pd.set_option('display.max_columns', None)
#import random
#random.seed(1)


def run():
    # Start time
    start = time.perf_counter()

    # Running tests from config file
    all_results = []
    for k, v in c.TESTS.items():
        print(f'---------------- {k} ------------------')
        # Run specific test case with N simulations
        results = AntSimulation(verbose=False, backtrack=v[1], diagonal=v[0], objective=v[2], name=k).run(c.N)
        # Analyze the data
        results.identify_distribution(plot=False)
        results.force_log_norm()
        # Store the results
        all_results.append(results)
    
    # Lognormal fit and comparison
    log_norms = ResultsAnalyzer.show_log_norm_fits(all_results)      
    ResultsAnalyzer.compare_log_norm(log_norms)

    # Store data in dataframe for future analysis e.g. easy csv/excel/database exports
    df = pd.DataFrame({x.name:x.output_data  for x in all_results}).T
    df['expectation'] = df['expectation'].astype(float)
    df['norm_mu'] = df['norm_mu'].astype(float)
    df['lognorm_expect'] = df['lognorm_expect'].astype(float)
    cols_to_keep = ['model_name', 'expectation', 'kstest_fitted', 'lognorm_kstest', 'lognorm_expect']

    result = df[cols_to_keep]
    result['Time (fit model)'] = (result['expectation']*10).round(2)
    result['Time (log norm)'] = (result['lognorm_expect']*10).round(2)
    print(result)
        
    # Measure performance stats
    end = time.perf_counter()
    print(f'Time taken: {end-start} seconds')
    plt.show(block=True)


if __name__ == '__main__':
    run()