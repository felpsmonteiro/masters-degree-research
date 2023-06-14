import os
import numpy as np
import pandas as pd
import seaborn as sns
import pickle as pkl
import err_metrics
import graphics
from tqdm import tqdm
 

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
            
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '.pkl')), 'rb') as f:
	            data = pkl.load(f)
            
            df_main = pd.DataFrame()
            
            errors_1 = {}  # DPNetTraffic + PostProcessing errors
            errors_2 = {}  # DPNetTraffic errors
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
                    errors_1[count][error_metr] = []
                    errors_2[count][error_metr] = []
                    errors_3[count][error_metr] = []
                    errors_4[count][error_metr] = []
                    errors_5[count][error_metr] = []
            
            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')
                
                errors_list_1 = {}  # approach
                errors_list_2 = {}  # approach_pp
                errors_list_3 = {}  # geometric
                errors_list_4 = {}  # log-laplace
                errors_list_5 = {}  # privbayes
                
                for count in self.counts:
                    errors_list_1[count] = {}
                    errors_list_2[count] = {}
                    errors_list_3[count] = {}
                    errors_list_4[count] = {}
                    errors_list_5[count] = {}

                    for error_metr in self.error_metrics:
                        errors_list_1[count][error_metr] = []
                        errors_list_2[count][error_metr] = []
                        errors_list_3[count][error_metr] = []
                        errors_list_4[count][error_metr] = []
                        errors_list_5[count][error_metr] = []

                
                for r in range(self.runs):

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_dpnettraffic_pp.pkl' % ( dataset, e, r ))), 'rb') as f:
                        data1 = pkl.load(f)
                    
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_dpnettraffic.pkl' % ( dataset, e, r ))), 'rb') as f:
                        data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_geometric.pkl' % ( dataset, e, r ))), 'rb') as f:
                        data3 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_log_laplace.pkl' % ( dataset, e, r ))), 'rb') as f:
                        data4 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_privbayes.pkl' % ( dataset, e, r ))), 'rb') as f:
                        data5 = pkl.load(f)

                    for error_metr in self.error_metrics:
                        for count in self.counts:
                            error_1 = err_metrics.calculate(error_metr, data[count], data1[count], k=None)
                            errors_list_1[count][error_metr].append(error_1)

                            error_2 = err_metrics.calculate(error_metr, data[count], data2[count], k=None)
                            errors_list_2[count][error_metr].append(error_2)

                            error_3 = err_metrics.calculate(error_metr, data[count], data3[count], k=None)
                            errors_list_3[count][error_metr].append(error_3)

                            error_4 = err_metrics.calculate(error_metr, data[count], data4[count], k=None)
                            errors_list_4[count][error_metr].append(error_4)
                            
                            error_5 = err_metrics.calculate(error_metr, data[count], data5[count], k=None)
                            errors_list_5[count][error_metr].append(error_5) 
                    
                for i in tqdm (range(self.runs), desc="Loading...", colour='blue'):
                    pass
                    
                df = pd.DataFrame({
                                    'Legends': pd.Series(dtype='str'),
                                    'Epsilon': pd.Series(dtype='float')
                                    })             

                for error_metr in self.error_metrics:
                    for count in self.counts:
                        
                        df[f"{count}_{error_metr}"] = pd.Series(dtype='float64')
                        
                        if df.empty:
                                ego_metric_mean_1 = errors_list_1[count][error_metr]
                                new_rows1 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_1, 'Legends': "DPNetTraffic + PostProcessing", 'Epsilon': e })
                                # df = df.append(new_rows1, ignore_index=True)
                                df = pd.concat([df, new_rows1], ignore_index=True)
                                
                                ego_metric_mean_2 = errors_list_2[count][error_metr]
                                new_rows2 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_2, 'Legends': "DPNetTraffic", 'Epsilon': e  })
                                df = pd.concat([df, new_rows2], ignore_index=True)
        
                                ego_metric_mean_3 = errors_list_3[count][error_metr]
                                new_rows3 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_3, 'Legends': "Mecanismo Geométrico", 'Epsilon': e  })
                                df = pd.concat([df, new_rows3], ignore_index=True)
                                                        
                                ego_metric_mean_4 = errors_list_4[count][error_metr]
                                new_rows4 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_4, 'Legends': "Mecanismo Log-Laplace", 'Epsilon': e  })
                                df = pd.concat([df, new_rows4], ignore_index=True)
                                
                                ego_metric_mean_5 = errors_list_5[count][error_metr]
                                new_rows5 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_5, 'Legends': "Privbayes", 'Epsilon': e  })
                                df = pd.concat([df, new_rows5], ignore_index=True)

                        else:
                                ego_metric_mean_1 = errors_list_1[count][error_metr]
                                df.iloc[0:50, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_1

                                ego_metric_mean_2 = errors_list_2[count][error_metr]
                                df.iloc[50:100, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_2

                                ego_metric_mean_3 = errors_list_3[count][error_metr]
                                df.iloc[100:150, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_3

                                ego_metric_mean_4 = errors_list_4[count][error_metr]
                                df.iloc[150:200, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_4
                                
                                ego_metric_mean_5 = errors_list_5[count][error_metr]
                                df.iloc[200:250, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_5

                df_main = pd.concat([df_main, df], ignore_index=True)
            
            df_main = df_main.reset_index()
            
            p1 = []
            p2 = []
            p3 = []
            p4 = []
            p5 = []

            for e in es:
                p1.append(df_main[f"{count}_{error_metr}"].loc[(df_main['Epsilon'] == e) & (df_main['Legends'] == 'DPNetTraffic + PostProcessing')].tolist())
                p2.append(df_main[f"{count}_{error_metr}"].loc[(df_main['Epsilon'] == e) & (df_main['Legends'] == 'DPNetTraffic')].tolist())
                p3.append(df_main[f"{count}_{error_metr}"].loc[(df_main['Epsilon'] == e) & (df_main['Legends'] == 'Mecanismo Geométrico')].tolist())
                p4.append(df_main[f"{count}_{error_metr}"].loc[(df_main['Epsilon'] == e) & (df_main['Legends'] == 'Mecanismo Log-Laplace')].tolist())
                p5.append(df_main[f"{count}_{error_metr}"].loc[(df_main['Epsilon'] == e) & (df_main['Legends'] == 'Privbayes')].tolist())
    
            for i in range(len(es)):
                print(f'\n--------- Calculating pvalue -- Epsilon: {es[i]} ---------')
                print(f"\t{count}_{error_metr}")
                
                print(f'DPPostProcessing + DPNetTraffic \n\tpvalue: {err_metrics.ttest(p1[i], p2[i])}')
                print(f'DPNetTraffic + Mecanismo Geométrico \n\tpvalue: {err_metrics.ttest(p2[i], p3[i])}')
                print(f'DPPostProcessing + Mecanismo Geométrico \n\tpvalue: {err_metrics.ttest(p1[i], p3[i])}')
                print(f'DPPostProcessing + Mecanismo Log-Laplace \n\tpvalue: {err_metrics.ttest(p1[i], p4[i])}')
                print(f'DPPostProcessing + Privbayes \n\tpvalue: {err_metrics.ttest(p1[i], p5[i])}')

if __name__ == "__main__":
    
    legends = [
                'DPNetTraffic + PostProcessing',
                'DPNetTraffic',
                'Mecanismo Geométrico',
                'Mecanismo Log-Laplace',
                'Privbayes'
            ]
    
    datasets = [
                'local',
                # 'cic', 
                # 'kaggle',
                # 'kagglel'
                ]

    error_metrics = [
                    # 'mae',
                    'mre'
                ]

    counts = [
                'protocols',
                # 'services',
                # 'ports'
            ]

    runs = 50
    
    es = [ .1, .5, 1 ]
    
    approach = Results(datasets, es, error_metrics, counts, runs)
    approach.run()
