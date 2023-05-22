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


class ResultsElapsedTime():

    def __init__(self, 
                    datasets,
                    es,
                    runs
                ):
        self.datasets = datasets
        self.es       = es
        self.runs     = runs

    def run(self):
        df = pd.read_pickle(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'elapsedtimes.pkl'))  )
                
        path_result = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', 'processingtime.png'))  
        graphics.plot_bar_graph(df, 'Dataset', 'ProcessingTime', xticksize=15, yticksize=15, line_legends='Legends', path=path_result, estimator=np.mean,
                                xlabel='Conjunto de Dados', xlabelfontsize=20, ylabel='Tempo de Processamento (seg)', ylabelfontsize=20,
                                legends_fontsize=30, ylog=True, themestyle='whitegrid', figwidth=12, figheight=8, place='upper left',
                                colors = ['#360CE8', '#4ECE00', '#FAA43A', '#F01F0F', '#AF10E0'])
if __name__ == "__main__":
    
    datasets = [
                'local',
                'kaggle',
                'kagglel'
                ]
    
    datasetsnames = {
                'local': 'Local',
                'kaggle': 'Labeled Network \nTraffic flows\n',
                'kagglel': 'IP Network Traffic \nFlows Labeled\n'
                    }

    es = [ .1, .5, 1 ] 

    runs = 50

    approach = ResultsElapsedTime(datasets, es, runs)
    approach.run()