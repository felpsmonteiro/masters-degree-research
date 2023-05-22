import os
import numpy as np
import pandas as pd
import warnings
# warnings.filterwarnings("ignore")
# pd.set_option('display.max_rows', 1000)
import seaborn as sns
import functions as fc
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
            
            errors_1 = {}  # approach errors
            errors_2 = {}  # geometric errors
            errors_3 = {}  # log-laplace errors
            errors_4 = {}  # privbayes errors

            for count in self.counts:
                errors_1[count] = {}
                errors_2[count] = {}
                errors_3[count] = {}
                errors_4[count] = {}
            
                for error_metr in self.error_metrics:
                    errors_1[count][error_metr] = []
                    errors_2[count][error_metr] = []
                    errors_3[count][error_metr] = []
                    errors_4[count][error_metr] = []
            
            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')
                
                errors_list_1 = {}  # approach
                errors_list_2 = {}  # geometric
                errors_list_3 = {}  # log-laplace
                errors_list_4 = {}  # privbayes

                for count in self.counts:
                    errors_list_1[count] = {}
                    errors_list_2[count] = {}
                    errors_list_3[count] = {}
                    errors_list_4[count] = {}

                    for error_metr in self.error_metrics:
                        errors_list_1[count][error_metr] = []
                        errors_list_2[count][error_metr] = []
                        errors_list_3[count][error_metr] = []
                        errors_list_4[count][error_metr] = []

                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_approach_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data1 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_geometric_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_log_laplace_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data3 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_privbayes_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data4 = pkl.load(f)

                    for error_metr in self.error_metrics:
                        for count in self.counts:
                            error_1 = err_metrics.calculate(error_metr, data[count], data1[count])
                            errors_list_1[count][error_metr].append(error_1)

                            error_2 = err_metrics.calculate(error_metr, data[count], data2[count])
                            errors_list_2[count][error_metr].append(error_2) 

                            error_3 = err_metrics.calculate(error_metr, data[count], data3[count])
                            errors_list_3[count][error_metr].append(error_3) 

                            error_4 = err_metrics.calculate(error_metr, data[count], data4[count])
                            errors_list_4[count][error_metr].append(error_4) 
                
                
                df = pd.DataFrame(columns=["Legends", "Epsilon"])
                
                for error_metr in self.error_metrics:
                    for count in self.counts:
                        
                        df[f"{count}_{error_metr}"] = pd.Series(dtype='float64')
                        
                        if df.empty:
                                ego_metric_mean_1 = errors_list_1[count][error_metr]
                                new_rows1 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_1, 'Legends': "Abordagem Proposta", 'Epsilon': e })
                                df = df.append(new_rows1, ignore_index=True)
                                
                                ego_metric_mean_2 = errors_list_2[count][error_metr]
                                new_rows2 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_2, 'Legends': "Mecanismo Geométrico", 'Epsilon': e  })
                                df = df.append(new_rows2, ignore_index=True)
        
                                ego_metric_mean_3 = errors_list_3[count][error_metr]
                                new_rows3 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_3, 'Legends': "Mecanismo Log-Laplace", 'Epsilon': e  })
                                df = df.append(new_rows3, ignore_index=True)
                                                        
                                ego_metric_mean_4 = errors_list_4[count][error_metr]
                                new_rows4 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_4, 'Legends': "Privbayes", 'Epsilon': e  })
                                df = df.append(new_rows4, ignore_index=True)

                        else:
                                ego_metric_mean_1 = errors_list_1[count][error_metr]
                                df.iloc[0:10, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_1

                                ego_metric_mean_2 = errors_list_2[count][error_metr]
                                df.iloc[10:20, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_2

                                ego_metric_mean_3 = errors_list_3[count][error_metr]
                                df.iloc[20:30, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_3

                                ego_metric_mean_4 = errors_list_4[count][error_metr]
                                df.iloc[30:40, df.columns.get_loc(f"{count}_{error_metr}")] = ego_metric_mean_4

                df_main = df_main.append(df)
            
            df_main = df_main.reset_index()
                        
            legends = [
                        'Abordagem Proposta',
                        'Mecanismo Geométrico',
                        'Mecanismo Log-Laplace',
                        'Privbayes'
                    ]

            for e in self.es:
                for error_metr in self.error_metrics:
                    for count in self.counts:
                        for l in legends:
                            
                            if error_metr == 'mre':
                            
                                media1 = df_main.loc[(df_main['Epsilon'] == e) & (df_main['Legends'] == l), f"{count}_{error_metr}"].mean()
                                print(dataset, "--", f"{count}_{error_metr}", "--", l, "--", e, "--", media1)                                
                            
                print('=' * 20)
                print('=' * 20)
            
            for error_metr in self.error_metrics:
                for count in self.counts:
                    print(df)
                    sns.set_theme(style="whitegrid")
                    colors = ['#360CE8', '#4ECE00', '#faa43a', '#F01F0F', '#AF10E0']
                    sns.set_palette(sns.color_palette(colors))
                    graph = sns.lineplot(data=df_main, x="Epsilon", y=f"{count}_{error_metr}",
                                         hue="Legends", style="Legends", err_style='band',
                                         markers=True, dashes=False)
                    graph.set_yscale('log')
                    # graph.set_title('$\epsilon$')
                    graph.set_xlabel('$\epsilon$', fontsize=20)
                    graph.set_ylabel(error_metr, fontsize=20)
                    graph.legend(fontsize=20)
                    # graph.set_xlim(0.0, 1.0)
                    fig = graph.get_figure()
                    fig.set_figwidth(7)
                    fig.set_figheight(7)  
                    fig.savefig(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', dataset,  error_metr, '%s_%s_%s_result_2_sns.png' % ( dataset, count, error_metr) )))
                    

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
