import os
import numpy as np

import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import warnings
import seaborn as sns
import pickle as pkl
import mechanisms
import err_metrics
import graphics
import matplotlib.pyplot as plt


class ElapsedTime():

    def __init__(self, 
                    datasets,
                    datasetsnames,
                    es,
                    runs
                ):
        self.datasets = datasets
        self.datasetsnames = datasetsnames
        self.es       = es
        self.runs     = runs

    def run(self):
        df = pd.DataFrame({'Dataset': pd.Series(dtype='str'),
                   'Legends': pd.Series(dtype='str'),
                   'Epsilon': pd.Series(dtype='float'),
                   'ProcessingTime': pd.Series(dtype='float')})

        for dataset in self.datasets:
            print('***************** DATASET ' + dataset + ' *****************')

            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_executiontime_preprocessing.pkl' % ( dataset))), 'rb') as f:
                data_ = pkl.load(f)

            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_approach.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data1 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_geometric.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_log_laplace.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data3 = pkl.load(f)
                            
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_privbayes.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data4 = pkl.load(f)
                                 
                    item1 = pd.DataFrame({'Dataset': dataset, 'Legends': 'Abordagem Proposta', 'Epsilon': e, 'ProcessingTime': data1['time'] + data_['time']}, index=[0])
                    df = pd.concat([df, item1], ignore_index=True)
                    
                    item2 = pd.DataFrame({'Dataset': dataset, 'Legends': 'Mecanismo Geométrico', 'Epsilon': e, 'ProcessingTime': data2['time'] + data_['time']}, index=[0])
                    df = pd.concat([df, item2], ignore_index=True)
                    
                    item3 = pd.DataFrame({'Dataset': dataset, 'Legends': 'Mecanismo Log-Laplace', 'Epsilon': e, 'ProcessingTime': data3['time'] + data_['time']}, index=[0])
                    df = pd.concat([df, item3], ignore_index=True)

                    item4 = pd.DataFrame({'Dataset': dataset, 'Legends': 'Privbayes', 'Epsilon': e, 'ProcessingTime': data4['time'] + data_['time']}, index=[0])
                    df = pd.concat([df, item4], ignore_index=True)

           
        df['Dataset'] = df['Dataset'].map(datasetsnames)
        
        path_df_save = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'elapsedtimes.pkl'))  
        df.to_pickle(path_df_save)
        
if __name__ == "__main__":
    
    datasets = [
                'local',
                'cic',
                'kaggle',
                'kagglel'
                ]
    
    datasetsnames = {
                'local': 'Local',
                'cic': 'Canadian Institute \nfor Cybersecurity',
                'kaggle': 'Labeled Network \nTraffic flows',
                'kagglel': 'IP Network Traffic \nFlows Labeled'
                    }

    es = [ .1, .5, 1 ] 

    runs = 50

    approach = ElapsedTime(datasets, datasetsnames, es, runs)
    approach.run()
