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
            
            #  0. Ler dados tabelão salvo pre processamento
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '_tab_2.pkl')), 'rb') as f:
                data2 = pkl.load(f)
         
            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    print('...... run ' + str(r) + ' ......')
                    
                    # 1. Add ruido no tabelão -- Nova coluna eps[e];
                    data2 = pd.DataFrame(data2, columns = ['DESTPORT','PROTOCOL','SERVICE', 'COUNT'])
                    data2[e] = mechanisms.geometric(data2['COUNT'].to_numpy(), e)
                                        
                    # 2. services_noisy = data2.groupby('SERVICE')[e].sum().to_numpy;
                    services_noisy = data2.groupby('SERVICE')[e].sum()
                    
                    # 3. protocols_noisy = data.groupby('PROTOCOL')[e].sum().to_numpy();
                    protocols_noisy = data2.groupby('PROTOCOL')[e].sum()
                    
                    # 4. ports_noisy = data.groupby('DESTPORT')[e].sum().to_numpy;
                    ports_noisy = data2.groupby('DESTPORT')[e].sum()
                   
                    protocols_post_processed = mechanisms.post_processing(protocols_noisy.to_numpy())
                    services_post_processed = mechanisms.post_processing(services_noisy.to_numpy())
                    ports_post_processed = mechanisms.post_processing(ports_noisy.to_numpy())

                    noisy_data = {
                        'protocols' : protocols_post_processed,
                        'services' : services_post_processed,
                        'ports' : ports_post_processed
                    }
                    
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', '%s_%s_%s_approach_2.pkl' % ( dataset, e, r ))), 'wb') as f:
	                    pkl.dump(noisy_data, f)

if __name__ == "__main__":

    datasets = [
                'local',
                'kaggle'    
                ]

    es = [ .01, .1, .5, 1 ] 

    runs = 10

    approach = ProposedApproach(datasets, es, runs)
    approach.run()
