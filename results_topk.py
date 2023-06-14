import os
import pandas as pd
import seaborn as sns
import numpy as np
import pickle as pkl
import err_metrics
import graphics
from tqdm import tqdm

class Results():

    def __init__(self, 
                    datasets,
                    es,
                    ks, 
                    error_metrics,
                    counts,
                    runs
                ):
        self.datasets = datasets 
        self.es = es 
        self.ks = ks 
        self.error_metrics = error_metrics 
        self.counts = counts 
        self.runs = runs 

    def run(self):
        for dataset in self.datasets:
            print('***************** DATASET ' + dataset + ' *****************')
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '.pkl')), 'rb') as f:
	            data = pkl.load(f)

            df_main = pd.DataFrame()
            
            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                errors_1 = {}  # approach postprocessing errors
                errors_2 = {}  # approach errors
                errors_3 = {}  # geometric errors
                errors_4 = {}  # log-laplace errors
                errors_5 = {}  # privbayes errors

                for count in self.counts:
                    errors_1[count] = {}
                    errors_2[count] = {}
                    errors_3[count] = {}
                    errors_4[count] = {}
                    errors_5[count] = {}
                
                    for error_metr in self.error_metrics:
                        errors_1[count][error_metr] = {}
                        errors_2[count][error_metr] = {}
                        errors_3[count][error_metr] = {}
                        errors_4[count][error_metr] = {}
                        errors_5[count][error_metr] = {}

                        for k in self.ks:
                            errors_1[count][error_metr][k] = []
                            errors_2[count][error_metr][k] = []
                            errors_3[count][error_metr][k] = []
                            errors_4[count][error_metr][k] = []
                            errors_5[count][error_metr][k] = []

                errors_list_1 = {}  # approach
                errors_list_2 = {}  # geometric
                errors_list_3 = {}  # log-laplace
                errors_list_4 = {}  # privbayes
                errors_list_5 = {}  # privbayes

                for count in self.counts:
                    errors_list_1[count] = {}
                    errors_list_2[count] = {}
                    errors_list_3[count] = {}
                    errors_list_4[count] = {}
                    errors_list_5[count] = {}

                    for error_metr in self.error_metrics:
                        errors_list_1[count][error_metr] = {}
                        errors_list_2[count][error_metr] = {}
                        errors_list_3[count][error_metr] = {}
                        errors_list_4[count][error_metr] = {}
                        errors_list_5[count][error_metr] = {}

                        for k in self.ks:
                            errors_list_1[count][error_metr][k] = []
                            errors_list_2[count][error_metr][k] = []
                            errors_list_3[count][error_metr][k] = []
                            errors_list_4[count][error_metr][k] = []
                            errors_list_5[count][error_metr][k] = []
                            

                for r in range(self.runs):
                    # print('...... run ' + str(r) + ' ......')

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_approach_pp.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data1 = pkl.load(f)
                    
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_approach.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset,'%s_%s_%s_geometric.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data3 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset,'%s_%s_%s_log_laplace.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data4 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset,'%s_%s_%s_privbayes.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data5 = pkl.load(f)
                    
                    for error_metr in self.error_metrics:
                        for count in self.counts:
                            for k in self.ks:
                                error_1 = err_metrics.calculate(error_metr, data[count], data1[count], k)
                                errors_list_1[count][error_metr][k].append(error_1)

                                error_2 = err_metrics.calculate(error_metr, data[count], data2[count], k)
                                errors_list_2[count][error_metr][k].append(error_2) 

                                error_3 = err_metrics.calculate(error_metr, data[count], data3[count], k)
                                errors_list_3[count][error_metr][k].append(error_3) 

                                error_4 = err_metrics.calculate(error_metr, data[count], np.array(data4[count]), k)
                                errors_list_4[count][error_metr][k].append(error_4) 
                                
                                error_5 = err_metrics.calculate(error_metr, data[count], np.array(data5[count]), k)
                                errors_list_5[count][error_metr][k].append(error_5) 
                
                for i in tqdm (range(self.runs), desc="Loading...", colour='blue'):
                        pass
                    
                for k in self.ks:
                    
                    df = pd.DataFrame({
                    'Legends': pd.Series(dtype='str'),
                    'Epsilon': pd.Series(dtype='float'),
                    'Ks': pd.Series(dtype='int')
                    })
                    
                    for count in self.counts:
                        df[f"{count}"] = pd.Series(dtype='float64')
                        
                        if df.empty:
                            ego_metric_mean_1 = errors_list_1[count][error_metr][k]
                            new_rows1 = pd.DataFrame({f"{count}": ego_metric_mean_1, 'Legends': "DPNetTraffic + PostProcessing", 'Epsilon': e, "Ks": k })
                            df = pd.concat([df, new_rows1], ignore_index=True)

                            ego_metric_mean_2 = errors_list_2[count][error_metr][k]
                            new_rows2 = pd.DataFrame({f"{count}": ego_metric_mean_2, 'Legends': "DPNetTraffic", 'Epsilon': e, "Ks": k })
                            df = pd.concat([df, new_rows2], ignore_index=True)
                            
                            ego_metric_mean_3 = errors_list_3[count][error_metr][k]
                            new_rows3 = pd.DataFrame({f"{count}": ego_metric_mean_3, 'Legends': "Mecanismo Geométrico", 'Epsilon': e, "Ks": k })
                            df = pd.concat([df, new_rows3], ignore_index=True)
                            
                            ego_metric_mean_4 = errors_list_4[count][error_metr][k]
                            new_rows4 = pd.DataFrame({f"{count}": ego_metric_mean_4, 'Legends': "Mecanismo Log-Laplace", 'Epsilon': e, "Ks": k })
                            df = pd.concat([df, new_rows4], ignore_index=True)
                            
                            ego_metric_mean_5 = errors_list_5[count][error_metr][k]
                            new_rows5 = pd.DataFrame({f"{count}": ego_metric_mean_5, 'Legends': "Privbayes", 'Epsilon': e, "Ks": k })
                            df = pd.concat([df, new_rows5], ignore_index=True)
                            
                            
                        else:
                            ego_metric_mean_1 = errors_list_1[count][error_metr][k]
                            df.iloc[0:50, df.columns.get_loc(f"{count}")] = ego_metric_mean_1

                            ego_metric_mean_2 = errors_list_2[count][error_metr][k]
                            df.iloc[50:100, df.columns.get_loc(f"{count}")] = ego_metric_mean_2

                            ego_metric_mean_3 = errors_list_3[count][error_metr][k]
                            df.iloc[100:150, df.columns.get_loc(f"{count}")] = ego_metric_mean_3

                            ego_metric_mean_4 = errors_list_4[count][error_metr][k]
                            df.iloc[150:200, df.columns.get_loc(f"{count}")] = ego_metric_mean_4
                            
                            ego_metric_mean_5 = errors_list_5[count][error_metr][k]
                            df.iloc[200:250, df.columns.get_loc(f"{count}")] = ego_metric_mean_5
                            
                
                    # df_main = df_main.append(df)
                    df_main = pd.concat([df_main, df], ignore_index=True)
                
                df_main = df_main.reset_index()
                         
            for error_metr in self.error_metrics:
                for count in self.counts:
                    
                    path_result = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', dataset, error_metr, '%s_%s_%s_result_log.png' % ( dataset, count, error_metr)))  
            
                    graphics.plot_line_graph(df_main, 'Ks', f'{count}', xticksize=12, yticksize=12, line_legends='Legends',
                                            path=path_result, xlabel='K', xlabelfontsize=15, ylabel='jaccard',
                                            ylabelfontsize=17, legends_fontsize=18, title=None, ylog=True, themestyle='whitegrid', error='band',
                                            figwidth=8, figheight=7, place='lower right', bottommargin=None, 
                                            colors = ['#41337F', '#360CE8', '#4ECE00', '#FAA43A', '#F01F0F'])

if __name__ == "__main__":

    datasets = [
                # 'cic',
                # 'local',
                'kaggle',
                'kagglel'
                ]
    legends = [
                'DPNetTraffic + PostProcessing',
                'DPNetTraffic',
                'Mecanismo Geométrico',
                'Mecanismo Log-Laplace',
                'Privbayes'
            ]

    error_metrics = [
                    'jaccard'
                ]

    counts = [
                # 'protocols',
                'services',
                'ports'
            ]

    runs = 50
    # es = [ .1, .5, 1 ]
    es = [ .1]

#Cic
    #Ports:
    # ks = [50, 100]
    #Services
    # ks = [1, 15]
    
#Local
    #Ports and Services
    # ks = [5, 20]

#Kaggle and #Kagglel
    #Ports and Services
    ks = [50, 100]

    approach = Results(datasets, es, ks, error_metrics, counts, runs)
    approach.run()