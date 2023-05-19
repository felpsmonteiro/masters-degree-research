import os
import time
import pandas as pd
import numpy as np
import pickle as pkl
import mechanisms


from DataSynthesizer.DataDescriber import DataDescriber
from DataSynthesizer.DataGenerator import DataGenerator
from DataSynthesizer.ModelInspector import ModelInspector
from DataSynthesizer.lib.utils import read_json_file, display_bayesian_network

class PrivBayes():

    def __init__(self, 
                    datasets,
                    size_dataset,
                    es,
                    runs,
                    datacsv,
                    sytheticdata
                ):
        self.datasets = datasets 
        self.size_dataset = size_dataset 
        self.es = es 
        self.runs = runs
        self.datacsv = datacsv
        self.sytheticdata = sytheticdata

    #### PrivBayes ####
    def privbayes(self, csv_path, threshold, catAttribute, candidateKeys, e, n, df_size, degree_bayesianNetwork):
            
        description_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', '{}.json'.format(description[0]) ))   # f'./{mode}/'
        synthetic_data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', '{}.csv'.format(sytheticdata[0]) )) #    f'./{mode}/'

        # An attribute is categorical if its domain size is less than this threshold.
        # Here modify the threshold to adapt to the domain size of "education" (which is 14 in input dataset).
        #threshold_value = 130
        threshold_value = threshold

        # specify categorical attributes
        #categorical_attributes = {'SERVICE': True, 'PROTOCOL': True, 'DESTPORT': True}
        categorical_attributes = catAttribute

        # specify which attributes are candidate keys of input dataset.
        candidate_keys = candidateKeys

        # A parameter in Differential Privacy. It roughly means that removing a row in the input dataset will not 
        # change the probability of getting the same output more than a multiplicative difference of exp(epsilon).
        # Increase epsilon value to reduce the injected noises. Set epsilon=0 to turn off differential privacy.
        epsilon = e

        # The maximum number of parents in Bayesian network, i.e., the maximum number of incoming edges.
        degree_of_bayesian_network = degree_bayesianNetwork

        # Number of tuples generated in synthetic dataset.
        num_tuples_to_generate = int(df_size) # Here 32561 is the same as input dataset, but it can be set to another number.

        describer = DataDescriber(category_threshold=threshold_value)
        describer.describe_dataset_in_correlated_attribute_mode(dataset_file=csv_path, 
                                                                epsilon=epsilon, 
                                                                k=degree_of_bayesian_network,
                                                                attribute_to_is_categorical=categorical_attributes,
                                                                attribute_to_is_candidate_key=candidate_keys)

        describer.save_dataset_description_to_file(description_path)

        display_bayesian_network(describer.bayesian_network)

        generator = DataGenerator()
        generator.generate_dataset_in_correlated_attribute_mode(num_tuples_to_generate, description_path, seed=n)
        generator.save_synthetic_data(synthetic_data_path)

        return synthetic_data_path

    def run(self):
        for dataset in self.datasets:
            print('***************** DATASET ' + dataset + ' *****************')

            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '.pkl')), 'rb') as f:
	            data = pkl.load(f)

            protocols, services, ports = data['protocols_names'], data['services_names'], data['ports_names']
            # prot_count, serv_count, ports_count = data['protocols'], data['services'], data['ports']

            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    starttime = time.time()

                    print('...... run ' + str(r) + ' ......')
                    
                    traf_df = pd.read_csv( os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', self.datasets[dataset] )) , sep=';', nrows = None)
                    traf_df_priv = traf_df[['DESTPORT', 'PROTOCOL', 'SERVICE']]

                    traf_df_priv.reset_index(inplace=True)
                    traf_df_priv = traf_df_priv.rename(columns={'index': 'INDEX_COLUMN'})
                    # traf_df_priv['INDEX_COLUMN'] = traf_df_priv.index
                    # traf_df_priv.reset_index
                    csv_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', '{}.csv'.format(datacsv[0]) ))
                    traf_df_priv.to_csv(csv_path)

                    threshold = int(len(traf_df_priv['SERVICE'].unique()) + 10)
                    cat_Attribute = {'DESTPORT': True, 'PROTOCOL': True, 'SERVICE': True}
                    candidateKeys = {'INDEX_COLUMN': True}

                    synthetic_data_path = self.privbayes(csv_path, threshold, cat_Attribute, candidateKeys, e, r, self.size_dataset*len(traf_df_priv), 2)
                    synthetic_data = pd.read_csv(synthetic_data_path)

                    synthetic_data["DESTPORT"] = pd.to_numeric(synthetic_data["DESTPORT"])

                    p_count, s_count, pr_count = [], [], []
                                    
                    traf_d_pt = synthetic_data.groupby('DESTPORT').count()['SERVICE']
                    traf_d_s = synthetic_data.groupby('SERVICE').count()['DESTPORT']
                    traf_d_p = synthetic_data.groupby('PROTOCOL').count()['DESTPORT']
                                    
                    for p in ports:
                        p_count.append(traf_d_pt[traf_d_pt.index == p].item())
                        
                    for s in services:
                        s_count.append(traf_d_s[traf_d_s.index == s].item())
                    
                    for pr in protocols:
                        pr_count.append(traf_d_p[traf_d_p.index == pr].item())

                    noisy_data = {
                        'protocols' : pr_count,
                        'services' : s_count,
                        'ports' : p_count
                    }

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_privbayes.pkl' % ( dataset, e, r ))), 'wb') as f:
	                    pkl.dump(noisy_data, f)
                    
                    endtime = time.time()

                    elapsed_time = endtime - starttime
        
                    print('Elapsed Time:', elapsed_time, 'seconds\n')

                    exectime = {
                                    'starttime' : starttime,
                                    'endtime' : endtime,
                                    'time' : elapsed_time
                                }
        
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_privbayes.pkl' % ( dataset, e, r ))), 'wb') as f:
                                    pkl.dump(exectime, f)

if __name__ == "__main__":

    datasets = {
        'kaggle': 'Unicauca-dataset-April-June-2019-Network-flows_2.csv'
        #'kagglel': 'Unicauca-dataset-April-June-2020-Network-flows_2.csv',
        #'local': 'traffic_table4.csv'
     }

    datacsv = [
        # 'privbayes1'
        'privbayes2'
        # 'privbayes3'
        # 'privbayes4'
        # 'privbayes5'
        # 'privbayes6'
        # 'privbayes7'
        # 'privbayes8'
        # 'privbayes9'
    ]

    sytheticdata = [
        # 'sythetic_data1' 
        'sythetic_data2' 
        # 'sythetic_data3' 
        # 'sythetic_data4' 
        # 'sythetic_data5' 
        # 'sythetic_data6' 
        # 'sythetic_data7' 
        # 'sythetic_data8' 
        # 'sythetic_data9' 
    ]

    description = [
        #  'description1'
         'description2'
        #  'description3'
        #  'description4'
        #  'description5'
        #  'description6'
        #  'description7'
        #  'description8'
        #  'description9'
    ]

    #es = [ .1, .5, 1 ] 
    es = [ .5 ] 

    runs = 50

    size_dataset = 1.0

    approach = PrivBayes(datasets, size_dataset, es, runs, datacsv, sytheticdata)
    approach.run()
