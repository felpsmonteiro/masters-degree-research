import os
import time
import pandas as pd
import pickle as pkl
import mechanisms


class Geometric():

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

            prot_count, serv_count, ports_count = data['protocols'], data['services'], data['ports']

            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    starttime = time.time()
                    
                    print('...... run ' + str(r) + ' ......')
                    
                    protocols_noisy = mechanisms.geometric(prot_count, e/3)
                    services_noisy = mechanisms.geometric(serv_count, e/3)
                    ports_noisy = mechanisms.geometric(ports_count, e/3)

                    noisy_data = {
                        'protocols' : protocols_noisy,
                        'services' : services_noisy,
                        'ports' : ports_noisy
                    }

                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_geometric.pkl' % ( dataset, e, r ))), 'wb') as f:
	                    pkl.dump(noisy_data, f)
                    
                    endtime = time.time()

                    elapsed_time = endtime - starttime
        
                    print('Elapsed Time:', elapsed_time, 'seconds\n')

                    exectime = {
                                    'starttime' : starttime,
                                    'endtime' : endtime,
                                    'time' : elapsed_time
                                }
        
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_geometric.pkl' % ( dataset, e, r ))), 'wb') as f:
                                    pkl.dump(exectime, f)

if __name__ == "__main__":

    datasets = [
                # 'local',
                'cic'
                # 'kaggle',
                # 'kagglel'
                ]

    es = [ .1, .5, 1 ] 

    runs = 50

    approach = Geometric(datasets, es, runs)
    approach.run()