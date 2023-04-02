import os
import pandas as pd
import numpy as np
import functions as fc
import pickle as pkl
import seaborn as sns
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
            
            # with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '_tab_2.pkl')), 'rb') as f:
	        #     data_ =  pd.DataFrame(pkl.load(f), columns = ['DESTPORT','PROTOCOL','SERVICE', 'COUNT'])
    
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
                
                for error_metr in self.error_metrics:
                    for count in self.counts:
                        ego_metric_mean_1 = np.mean(errors_list_1[count][error_metr])
                        errors_1[count][error_metr].append(float("{:.2f}".format(ego_metric_mean_1)))

                        ego_metric_mean_2 = np.mean(errors_list_2[count][error_metr])
                        errors_2[count][error_metr].append(float("{:.2f}".format(ego_metric_mean_2)))

                        ego_metric_mean_3 = np.mean(errors_list_3[count][error_metr])
                        errors_3[count][error_metr].append(float("{:.2f}".format(ego_metric_mean_3)))

                        ego_metric_mean_4 = np.mean(errors_list_4[count][error_metr])
                        errors_4[count][error_metr].append(float("{:.2f}".format(ego_metric_mean_4)))
                        
                # for error_metr in self.error_metrics:
                #     df1 = pd.DataFrame()
                #     df2 = pd.DataFrame()
                #     df3 = pd.DataFrame()
                #     df4 = pd.DataFrame()
                                     
                #     for count in self.counts:
                #         ego_metric_mean_1 = errors_list_1[count][error_metr]
                #         df1[f"{count}_{error_metr}"] = ego_metric_mean_1
                        
                #         ego_metric_mean_2 = errors_list_2[count][error_metr]
                #         df2[f"{count}_{error_metr}"] = ego_metric_mean_2
                        
                #         ego_metric_mean_3 = errors_list_3[count][error_metr]
                #         df3[f"{count}_{error_metr}"] = ego_metric_mean_3

                #         ego_metric_mean_4 = errors_list_4[count][error_metr]
                #         df4[f"{count}_{error_metr}"] = ego_metric_mean_4

            legends = [
                        'Abordagem Proposta',
                        'Mecanismo Geométrico',
                        'Mecanismo Log-Laplace',
                        'Privbayes'
                    ]

            for error_metr in self.error_metrics:
                for count in self.counts:
                    y = []
                    y.append(errors_1[count][error_metr])
                    y.append(errors_2[count][error_metr])
                    y.append(errors_3[count][error_metr])
                    y.append(errors_4[count][error_metr])
                    
                    # data = {'y': y, 'x': legends}
                    # df = pd.DataFrame(data)
                    # print(df)
                    # df = pd.DataFrame(my_array, columns = ['Column_A','Column_B','Column_C'])
                    # print(dataset, error_metr , count), print(y)
 
                    path_result = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', dataset, error_metr, '%s_%s_%s_result_log_2.png' % ( dataset, count, error_metr) ))  
                    graphics.line_plot(np.array(self.es), np.array(y), xlabel='$\epsilon$', ylabel= error_metr, ylog=True, line_legends=legends, figsize=(5, 5), path=path_result)

                    path_result2 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', dataset,  error_metr, '%s_%s_%s_result_2.png' % ( dataset, count, error_metr) ))  
                    graphics.line_plot(np.array(self.es), np.array(y), xlabel='$\epsilon$', ylabel= error_metr, ylog=False, line_legends=legends, figsize=(5, 5), path=path_result2)

if __name__ == "__main__":

    datasets = [
                'kaggle',
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
