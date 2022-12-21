import os
import pandas as pd
import numpy as np
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
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '.pkl')), 'rb') as f:
	            data = pkl.load(f)

            # original data
            # protocols, services, ports = data[0], data[1], data[2]
            # prot_count, serv_count, ports_count = data[3], data[4], data[5]

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

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', '%s_%s_%s_approach.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data1 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', '%s_%s_%s_geometric.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', '%s_%s_%s_log_laplace.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data3 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', '%s_%s_%s_privbayes.pkl' % ( dataset, e, r ))), 'rb') as f:
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

                    path_result = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', '%s_%s_%s_result_log.png' % ( dataset, count, error_metr) ))  
                    graphics.line_plot(np.array(self.es), np.array(y), xlabel='$\epsilon$', ylabel= error_metr, ylog=True, line_legends=legends, figsize=(5, 5), path=path_result)

                    path_result2 = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', '%s_%s_%s_result.png' % ( dataset, count, error_metr) ))  
                    graphics.line_plot(np.array(self.es), np.array(y), xlabel='$\epsilon$', ylabel= error_metr, ylog=False, line_legends=legends, figsize=(5, 5), path=path_result2)

if __name__ == "__main__":

    datasets = [
                #'local',
                'kaggle'    
                ]

    es = [ .01, .1, .5, 1 ] 

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
