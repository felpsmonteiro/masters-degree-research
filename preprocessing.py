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
        traf_df["DESTPORT"] = pd.to_numeric(traf_df["DESTPORT"])
        protocol, service, ports = traf_df['PROTOCOL'].unique(), np.array(traf_df['SERVICE'].unique()), np.array(traf_df['DESTPORT'].unique())
        prot_count, serv_count, ports_count = fc.Count(protocol, traf_df, "PROTOCOL"), fc.Count(service, traf_df, "SERVICE"), fc.Count(ports, traf_df, "DESTPORT")
        
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

if __name__ == "__main__":

    # url_local = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'Unicauca-dataset-April-June-2019-Network-flows.csv' ))
    url_local = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Datasets', 'traffic_table4.csv' ))
    pre_proc_local = PreProcessing(url_local, 'local' )
    pre_proc_local.preprocess_dataset()
