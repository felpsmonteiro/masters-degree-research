import os
import pandas as pd
import numpy as np
import functions as fc
import pickle as pkl
import mechanisms

class LogLaplace():

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
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '_2.pkl')), 'rb') as f:
	            data = pkl.load(f)

            # protocols, services, ports = data[0], data[1], data[2]
            prot_count, serv_count, ports_count = data['protocols'], data['services'], data['ports']

            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')
                    protocols_noisy = mechanisms.log_laplace(prot_count, e/3)
                    services_noisy = mechanisms.log_laplace(serv_count, e/3)
                    ports_noisy = mechanisms.log_laplace(ports_count, e/3)

                    noisy_data = {
                        'protocols' : protocols_noisy,
                        'services' : services_noisy,
                        'ports' : ports_noisy
                    }

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_log_laplace_2.pkl' % ( dataset, e, r ))), 'wb') as f:
	                    pkl.dump(noisy_data, f)

if __name__ == "__main__":

    datasets = [
                'local',
                'kaggle'    
                ]

    es = [ .1, .5, 1 ] 

    runs = 10

    approach = LogLaplace(datasets, es, runs)
    approach.run()
