import os
import pandas as pd
import numpy as np
import pickle as pkl
import mechanisms
import time

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
            with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', dataset + '_tab.pkl')), 'rb') as f:
                data = pkl.load(f)
         
            for e in self.es:
                print('--------- eps ' + str(e) + ' ---------')

                for r in range(self.runs):
                    starttime = time.time()
                    
                    print('...... run ' + str(r) + ' ......')
                    
                    # 1. Add ruido no tabelão -- Nova coluna eps[e];
                    # data = pd.DataFrame(data, columns = ['DESTPORT','PROTOCOL','SERVICE', 'COUNT'])
                    data[e] = mechanisms.geometric(data['COUNT'].to_numpy(), e)
                                        
                    # 2. services_noisy = data2.groupby('SERVICE')[e].sum().to_numpy;
                    services_noisy = data.groupby('SERVICE')[e].sum()
                    
                    # 3. protocols_noisy = data.groupby('PROTOCOL')[e].sum().to_numpy();
                    protocols_noisy = data.groupby('PROTOCOL')[e].sum()
                    
                    # 4. ports_noisy = data.groupby('DESTPORT')[e].sum().to_numpy;
                    ports_noisy = data.groupby('DESTPORT')[e].sum()

                    services_post_processed = mechanisms.post_processing(services_noisy.to_numpy())
                    protocols_post_processed = mechanisms.post_processing(protocols_noisy.to_numpy())
                    ports_post_processed = mechanisms.post_processing(ports_noisy.to_numpy())
                    # np.clip(level_noisy_p_apr[e][at][lv], 1, None)
                    
                    noisy_data = {
                        'protocols' : protocols_post_processed,
                        'services' : services_post_processed,
                        'ports' : ports_post_processed
                    }
                    
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_approach.pkl' % ( dataset, e, r ))), 'wb') as f:
	                    pkl.dump(noisy_data, f)
                    
                    endtime = time.time()
                    elapsed_time = endtime - starttime
        
                    print('Elapsed Time:', elapsed_time, 'seconds\n')

                    exectime = {
                                    'starttime' : starttime,
                                    'endtime' : endtime,
                                    'time' : elapsed_time
                                }
        
                    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', dataset, '%s_%s_%s_executiontime_approach.pkl' % ( dataset, e, r ))), 'wb') as f:
                                    pkl.dump(exectime, f)
                                    
if __name__ == "__main__":

    datasets = [
                'local',
                'unsw',
                'kaggle',
                'kagglel'
                ]

    es = [ .1, .5, 1 ] 

    runs = 50

    approach = ProposedApproach(datasets, es, runs)
    approach.run()
