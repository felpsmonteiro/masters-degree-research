import os
import numpy as np
# import pandas as pd
# import math
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# import seaborn as snspi

# from DataSynthesizer.DataDescriber import DataDescriber
# from DataSynthesizer.DataGenerator import DataGenerator
# from DataSynthesizer.ModelInspector import ModelInspector
# from DataSynthesizer.lib.utils import read_json_file, display_bayesian_network

# import warnings
# warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 

def Count(array, df, colname):
    data_arr = []
    
    for i in array:
        data_arr.append(df[df[colname] == i].shape[0])

    return np.array(data_arr)

# # def Geometric_Mechanism(arr, eps, sensitivity):
    
# #     p = 1 - np.exp(-eps/sensitivity) 
# #     noise = np.random.geometric(p, len(arr)) - np.random.geometric(p, len(arr))
    
# #     arr_noisy = arr + noise
    
# #     return arr_noisy

# # def log_laplace_mechanism(arr, eps, sensitivity):
# #     lap = np.random.laplace(loc=0, scale=sensitivity/eps, size=len(arr))
# #     #  noisy_arr = np.around(np.clip( np.log(arr) + lap, 1, None )).astype(int)
# #     noisy_arr = np.around(np.clip(arr * np.exp(lap), 1, max(arr))).astype(int)  # https://arxiv.org/pdf/2101.02957.pdf

# #     return np.array(noisy_arr)

# # # Mean Absolute Error
# # def mae(arr_true, arr_pred):       
# #     error = np.mean( np.abs(arr_true - arr_pred) )
# #     return error

# # # Mean Relative Error
# # def mre(arr_true, arr_pred):     
# #     error = np.mean( np.abs(arr_pred - arr_true ) / arr_true  )
    
# #     return error

# # def GetError(arraycount):
# #     ep = [0.1, 0.5, 1]

# #     array_count_noisy = []

# #     mae_geom = []
# #     mre_geom = []

# #     for e in ep:
# #         noisy_ep = []

# #         for t in range(100):
# #             gm = Geometric_Mechanism(arraycount, e, 1)
# #             noisy_ep.append(np.array(gm))

# #         array_count_noisy.append(noisy_ep)

# #     for i in range(len(ep)):

# #         mae_ep = []
# #         mre_ep = []

# #         for t in range(100):
# #             mae_ep.append(mae(arraycount, array_count_noisy[i][t]))
# #             mre_ep.append(mre(arraycount, array_count_noisy[i][t]))

# #         mae_geom.append(mae_ep)
# #         mre_geom.append(mre_ep)

# #     mean_mae = np.mean(np.array(mae_geom), axis=1)
# #     mean_mre = np.mean(np.array(mre_geom), axis=1)
    
# #     return array_count_noisy, mae_geom, mre_geom, mean_mae, mean_mre

# # def line_plot(x, ys, path=None, line_legends=None, legend_path=None, 
# #               xlabel=None, ylabel=None, title=None, xlog=False, ylog=False,
# #               linestyles = [':', '--', '-.', (0, (3, 1, 1, 1, 1, 1)), ':', 
# #                             'dashed', ':', '--', '-.', 'dashed'],
# #               colors = ['#000000', '#360CE8', '#4ECE00', '#FF0000', 
# #                         '#FF69B4', '#FFFF00', '#00009F', '#F3F0F0', 
# #                         '#AF10E0', '#F01F0F'],
# #               markers = ['o','x','+','>','1','v','d','o','d','1'],
# #               figsize=(9, 6),
# #               ylim=None):

# #     fig, ax = plt.subplots(figsize=figsize, tight_layout=True)

# #     if markers is None:
# #         markers = ["None"]*len(ys)

# #     if linestyles is None:
# #         linestyles = ['-']*len(ys)
    
# #     if line_legends is None:
# #         line_legends = [None]*len(ys)
    
# #     lines = []
# #     for i,y in enumerate(ys):    
# #         lines.append(
# #             ax.plot(x, y, 
# #                 linestyle=linestyles[i],
# #                 linewidth=1.5, 
# #                 color=colors[i],
# #                 label=line_legends[i]
# #                 # marker=markers[i]
# #             )
# #         )

# #     plt.legend()
# #     if ylog:
# #         plt.yscale('log')    
# #     # if xlog:
# #         # plt.xscale('log')    
# #     if ylabel:
# #         ax.set_ylabel(ylabel)
# #     if xlabel:
# #         ax.set_xlabel(xlabel)
# #     if title:
# #         ax.set_title(title)
# #     if ylim is not None:
# #         ax.set_ylim(ylim)
# #     ax.grid(True)
    
# #     if path:
# #         dir_path = os.path.dirname(os.path.realpath(path))
# #         os.makedirs(dir_path, exist_ok=True)
# #         plt.savefig(path, dpi=900)
# #         print('Graphic saved at: ' + path)
# #     else:
# #         plt.show()
# #     plt.clf()
# #     plt.close()
    
# # #### PrivBayes ####
# # def syntheticData(dfType, df, threshold, catAttribute, candidateKeys, e, n, df_size, degree_bayesianNetwork):
# #     input_data = df
# #     #input_data = 'privb_test.csv'
    
# #     if dfType == 'Local' or 'Kaggle':
# #         # location of two output files
        
# #         if os.path.exists(f'{dfType}/{e}/'):
# #             print('=' * 30)
# #             print(f'{dfType}/{e}/')
# #             print('=' * 30)
        
# #         else:
# #             os.makedirs(f'{dfType}/{e}/')
            
# #             print('=' * 30)
# #             print(f'Creating path {dfType}/{e}/')
# #             print('=' * 30)
    
# #     else: print('THE DATASET TYPE HAS NoT BEEN SPECIFIED')
    
# #     mode = f'{dfType}/{e}/'
           
# #     description_file = f'{mode}/description_{n}.json'
# #     synthetic_data = f'{mode}/sythetic_data_{n}.csv'

# #     # An attribute is categorical if its domain size is less than this threshold.
# #     # Here modify the threshold to adapt to the domain size of "education" (which is 14 in input dataset).
# #     #threshold_value = 130
# #     threshold_value = threshold

# #     # specify categorical attributes
# #     #categorical_attributes = {'SERVICE': True, 'PROTOCOL': True, 'DESTPORT': True}
# #     categorical_attributes = catAttribute

# #     # specify which attributes are candidate keys of input dataset.
# #     candidate_keys = candidateKeys

# #     # A parameter in Differential Privacy. It roughly means that removing a row in the input dataset will not 
# #     # change the probability of getting the same output more than a multiplicative difference of exp(epsilon).
# #     # Increase epsilon value to reduce the injected noises. Set epsilon=0 to turn off differential privacy.
# #     epsilon = e

# #     # The maximum number of parents in Bayesian network, i.e., the maximum number of incoming edges.
# #     degree_of_bayesian_network = degree_bayesianNetwork

# #     # Number of tuples generated in synthetic dataset.
# #     num_tuples_to_generate = df_size # Here 32561 is the same as input dataset, but it can be set to another number.

# #     describer = DataDescriber(category_threshold=threshold_value)
# #     describer.describe_dataset_in_correlated_attribute_mode(dataset_file=input_data, 
# #                                                             epsilon=epsilon, 
# #                                                             k=degree_of_bayesian_network,
# #                                                             attribute_to_is_categorical=categorical_attributes,
# #                                                             attribute_to_is_candidate_key=candidate_keys)

# #     describer.save_dataset_description_to_file(description_file)

# #     display_bayesian_network(describer.bayesian_network)

# #     generator = DataGenerator()
# #     generator.generate_dataset_in_correlated_attribute_mode(num_tuples_to_generate, description_file, seed=n)
# #     generator.save_synthetic_data(synthetic_data)

# #     # Read both datasets using Pandas.
# #     input_df = pd.read_csv(input_data, skipinitialspace=True)
# #     synthetic_df = pd.read_csv(synthetic_data)
# #     # Read attribute description from the dataset description file.
# #     attribute_description = read_json_file(description_file)['attribute_description']

# #     inspector = ModelInspector(input_df, synthetic_df, attribute_description)

# #     return inspector