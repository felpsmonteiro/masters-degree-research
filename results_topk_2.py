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
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '_2.pkl')), 'rb') as f:
	            data = pkl.load(f)

            # original data
            # protocols, services, ports = data[0], data[1], data[2]
            # prot_count, serv_count, ports_count = data[3], data[4], data[5]

            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

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
                        errors_1[count][error_metr] = {}
                        errors_2[count][error_metr] = {}
                        errors_3[count][error_metr] = {}
                        errors_4[count][error_metr] = {}

                        for k in self.ks:
                            errors_1[count][error_metr][k] = []
                            errors_2[count][error_metr][k] = []
                            errors_3[count][error_metr][k] = []
                            errors_4[count][error_metr][k] = []

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
                        errors_list_1[count][error_metr] = {}
                        errors_list_2[count][error_metr] = {}
                        errors_list_3[count][error_metr] = {}
                        errors_list_4[count][error_metr] = {}

                        for k in self.ks:
                            errors_list_1[count][error_metr][k] = []
                            errors_list_2[count][error_metr][k] = []
                            errors_list_3[count][error_metr][k] = []
                            errors_list_4[count][error_metr][k] = []
                            

                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_approach_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data1 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset,'%s_%s_%s_geometric_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data2 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset,'%s_%s_%s_log_laplace_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data3 = pkl.load(f)

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset,'%s_%s_%s_privbayes_2.pkl' % ( dataset, e, r ))), 'rb') as f:
	                    data4 = pkl.load(f)

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

                df = pd.DataFrame(columns=["Legends", "Epsilon", "Ks"])
                
                for error_metr in self.error_metrics:
                    for count in self.counts:
                        
                        df[f"{count}_{error_metr}"] = pd.Series(dtype='float64')
                        
                        if df.empty:
                                ego_metric_mean_1 = errors_list_1[count][error_metr]
                                new_rows1 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_1, 'Legends': "Abordagem Proposta", 'Epsilon': e, "Ks": k })
                                df = df.append(new_rows1, ignore_index=True)
                                
                                ego_metric_mean_2 = errors_list_2[count][error_metr]
                                new_rows2 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_2, 'Legends': "Mecanismo Geométrico", 'Epsilon': e, "Ks": k  })
                                df = df.append(new_rows2, ignore_index=True)
        
                                ego_metric_mean_3 = errors_list_3[count][error_metr]
                                new_rows3 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_3, 'Legends': "Mecanismo Log-Laplace", 'Epsilon': e, "Ks": k  })
                                df = df.append(new_rows3, ignore_index=True)
                                                        
                                ego_metric_mean_4 = errors_list_4[count][error_metr]
                                new_rows4 = pd.DataFrame({f"{count}_{error_metr}": ego_metric_mean_4, 'Legends': "Privbayes", 'Epsilon': e, "Ks": k })
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

            legends = [
                        'Abordagem Proposta',
                        'Mecanismo Geométrico',
                        'Mecanismo Log-Laplace',
                        'Privbayes'
                    ]

            for error_metr in self.error_metrics:
                for count in self.counts:
                    # for k in self.ks:
                    # y = []
                    # y.append(errors_1[count][error_metr].values())
                    # y.append(errors_2[count][error_metr].values())
                    # y.append(errors_3[count][error_metr].values())
                    # y.append(errors_4[count][error_metr].values())
                    
                    sns.set_theme(style="darkgrid")
                    # graph.set(yscale='log')
                    graph = sns.lineplot(data=df_main, x="Epsilon", y=f"{count}_{error_metr}",
                                         hue="Legends", style="Legends", err_style='bars',
                                         markers=True, dashes=False)
                    graph.set_yscale('log')
                    # graph.set_title('$\epsilon$')
                    graph.set_xlabel('$\epsilon$')
                    graph.set_ylabel(error_metr)
                    fig = graph.get_figure()
                    fig.savefig(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', '%s_%s_%s_%s_result_topk_2.png' % ( dataset, count, error_metr, k) )))

                    path_result = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'results', '%s_%s_%s_%s_result_topk_2.png' % ( dataset, count, error_metr, k) ))  
                    graphics.line_plot(np.array(self.ks), np.array(y), xlabel='k', ylabel= error_metr, ylog=False, line_legends=legends, figsize=(7, 5), path=path_result)


if __name__ == "__main__":

    datasets = [
                'local',
                'kaggle'    
                ]

    es = [ .1, .5, 1 ] 

    ks = [50]
    #ks = [10, 25, 50, 75, 100]

    error_metrics = [
                    'jaccard'
                ]

    counts = [
                'protocols',
                'services',
                'ports'
            ]

    runs = 10

    approach = Results(datasets, es, ks, error_metrics, counts, runs)
    approach.run()