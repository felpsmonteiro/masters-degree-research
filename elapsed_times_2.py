import os
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_rows', 1000)
import seaborn as sns

import pickle as pkl
import mechanisms
import err_metrics
import graphics


class Results():

    def __init__(self, 
                    datasets,
                    es,
                    error_metrics,
                    counts,
                    runs
                ):
        self.datasets = datasets 
        self.es = es 
        self.error_metrics = error_metrics 
        self.counts = counts 
        self.runs = runs 

    def run(self):
        for dataset in self.datasets:
            print('***************** DATASET ' + dataset + ' *****************')
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '_2.pkl')), 'rb') as f:
	            data = pkl.load(f)
            
            df_main = pd.DataFrame()
            
            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')
                
                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_approach_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data1 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_geometric_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_log_laplace_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data3 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_privbayes_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data4 = pkl.load(f)


if __name__ == "__main__":

    datasets = [
                'kaggle',
                'kagglel',
                'local'    
                ]

    es = [ .1, .5, 1 ] 

    error_metrics = [
                    'mae',
                    'mre'
                ]

    counts = [
                'protocols',
                'services',
                'ports'
            ]

    runs = 10

    approach = Results(datasets, es, error_metrics, counts, runs)
    approach.run()
