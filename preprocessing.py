import os
import pandas as pd
import numpy as np
import pickle as pkl
import time

class PreProcessing():

    def __init__(self, 
                    dataset_url,
                    dataset_name
                ):
        self.dataset_url = dataset_url 
        self.dataset_name = dataset_name 

    def preprocess_dataset(self):
        
        starttime = time.time()
        
        traf_df = pd.read_csv(self.dataset_url, sep=';', nrows=None)
        
        df_counts = traf_df.groupby(['DESTPORT', 'PROTOCOL', 'SERVICE']).size().reset_index(name='COUNT')
        # df_counts = traf_df.sort_values(['DESTPORT'],ascending=False).groupby(['DESTPORT', 'PROTOCOL', 'SERVICE']).size().reset_index(name='COUNT')
        
        df_prot = traf_df.groupby(['PROTOCOL']).size().reset_index(name='COUNT')
        df_serv = traf_df.groupby(['SERVICE']).size().reset_index(name='COUNT')
        df_port = traf_df.groupby(['DESTPORT']).size().reset_index(name='COUNT')
        
        protocol = df_prot['PROTOCOL'].to_numpy()
        service = df_serv['SERVICE'].to_numpy()
        ports = df_port['DESTPORT'].to_numpy()

        prot_count = df_prot['COUNT'].to_numpy()
        serv_count = df_serv['COUNT'].to_numpy()
        ports_count = df_port['COUNT'].to_numpy()

        new_data = {
                        'protocols' : prot_count,
                        'services' : serv_count,
                        'ports' : ports_count,
                        'protocols_names' : protocol,
                        'services_names' : service,
                        'ports_names' : ports
                    }
        
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', self.dataset_name + '.pkl')), 'wb') as f:
            pkl.dump(new_data, f)
        
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', self.dataset_name + '_tab.pkl')), 'wb') as f:
            pkl.dump(df_counts, f)
        
        endtime = time.time()
        elapsed_time = endtime - starttime

        print(self.dataset_name,'\nElapsed Time:', elapsed_time, 'seconds\n')

        exectime = {
                        'starttime' : starttime,
                        'endtime' : endtime,
                        'time' : elapsed_time
                    }

        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'exp', self.dataset_name, '%s_executiontime_preprocessing.pkl' % ( self.dataset_name ))), 'wb') as f:
                        pkl.dump(exectime, f)        
        

if __name__ == "__main__":

    # url_kaggle = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'Unicauca-dataset-April-June-2019-Network-flows.csv' ))
    #     #https://www.kaggle.com/datasets/jsrojas/ip-network-traffic-flows-labeled-with-87-apps
    
    url_unsw = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'NUSW-NB15_GT.csv' ))
    #     #UNSW-NB15: Este conjunto de dados contém dados de tráfego de rede capturados em um ambiente de laboratório simulado. 
    #     # Ele é frequentemente usado para pesquisa em detecção de intrusões e análise de tráfego.
    #     #https://research.unsw.edu.au/projects/unsw-nb15-dataset
    
    # url_kagglel = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'Unicauca-dataset-April-June-2020-Network-flows_2.csv' ))
    #     #Labeled Network Traffic flows -- 1.28GB
    #     #https://www.kaggle.com/datasets/jsrojas/labeled-network-traffic-flows-114-applications
    
    # url_local = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'traffic_table.csv' ))
    
    # pre_proc_kaggle = PreProcessing(url_kaggle, 'kaggle')
    pre_proc_unsw = PreProcessing(url_unsw, 'unsw')
    # pre_proc_kagglel = PreProcessing(url_kagglel, 'kagglel')
    # pre_proc_local = PreProcessing(url_local, 'local')
    
    # pre_proc_kaggle.preprocess_dataset()
    pre_proc_unsw.preprocess_dataset()
    # pre_proc_kagglel.preprocess_dataset()
    # pre_proc_local.preprocess_dataset()