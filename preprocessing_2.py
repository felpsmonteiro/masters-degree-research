import os
import pandas as pd
import numpy as np
import functions as fc
import pickle as pkl

class PreProcessing():

    def __init__(self, 
                    dataset_url,
                    dataset_name
                ):
        self.dataset_url = dataset_url 
        self.dataset_name = dataset_name 

    def preprocess_dataset(self):
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
        
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', self.dataset_name + '_2.pkl')), 'wb') as f:
            pkl.dump(new_data, f)
        
        with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', self.dataset_name + '_tab_2.pkl')), 'wb') as f:
            pkl.dump(df_counts, f)


if __name__ == "__main__":

    url_kaggle = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'Unicauca-dataset-April-June-2019-Network-flows.csv' ))
    url_kagglel = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'Unicauca-dataset-April-June-2020-Network-flows_2.csv' ))
    url_local = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'traffic_table4.csv' ))
    pre_proc_kaggle = PreProcessing(url_kaggle, 'kaggle')
    pre_proc_kagglel = PreProcessing(url_kaggle, 'kagglel')
    pre_proc_local = PreProcessing(url_local, 'local' )
    pre_proc_kaggle.preprocess_dataset()
    pre_proc_kagglel.preprocess_dataset()
    pre_proc_local.preprocess_dataset()