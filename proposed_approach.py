import os
import pandas as pd
import numpy as np
import functions as fc
import pickle as pkl
import mechanisms

class ProposedApproach():

    def __init__(self, 
                    datasets,
                    es,
                    runs
                ):
        self.datasets = datasets 
        self.es = es 
        self.runs = runs 

    def run(self):
        for dataset in self.datasets:
            print('***************** DATASET ' + dataset + ' *****************')
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '.pkl')), 'rb') as f:
	            data = pkl.load(f)

            # protocols, services, ports = data[0], data[1], data[2]
            prot_count, serv_count, ports_count = data['protocols'], data['services'], data['ports']

            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')
                    protocols_noisy = mechanisms.geometric(prot_count, e)
                    services_noisy = mechanisms.geometric(serv_count, e)
                    ports_noisy = mechanisms.geometric(ports_count, e)

                    protocols_post_processed = mechanisms.post_processing(protocols_noisy)
                    services_post_processed = mechanisms.post_processing(services_noisy)
                    ports_post_processed = mechanisms.post_processing(ports_noisy)

                    noisy_data = {
                        'protocols' : protocols_post_processed,
                        'services' : services_post_processed,
                        'ports' : ports_post_processed
                    }
                    
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', '%s_%s_%s_approach.pkl' % ( dataset, e, r ))), 'wb') as f:
	                    pkl.dump(noisy_data, f)

if __name__ == "__main__":

    datasets = [
                # 'local',
                'kaggle'    
                ]

    es = [ .01, .05, .1, .5, 1 ] 

    runs = 10

    approach = ProposedApproach(datasets, es, runs)
    approach.run()
