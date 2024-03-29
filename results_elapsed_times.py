import os
import graphics
import pandas as pd
import numpy as np
import pickle as pkl

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
                                legends_fontsize=17, ylog=True, themestyle='whitegrid', figwidth=15, figheight=9, place='upper left', errorb=('ci', 95),
                                # colors = ['#360CE8', '#4ECE00', '#FAA43A', '#F01F0F'])
                                colors = ['#564A8E', '#5A3AEC', '#78CE43', '#F0B063', '#F35448']) #41337F   #564A8E
if __name__ == "__main__":
    
    datasets = [
                'local',
                'cic',
                'kaggle',
                'kagglel'
                ]
    
    datasetsnames = {
                'local': 'Local Laboratory \nTraffic Flow',
                'cic': 'Canadian Institute \nfor Cybersecurity',
                'kaggle': 'Labeled Network \nTraffic flows',
                'kagglel': 'IP Network Traffic \nFlows Labeled'
                    }

    es = [ .1, .5, 1 ] 

    runs = 50

    approach = ResultsElapsedTime(datasets, es, runs)
    approach.run()