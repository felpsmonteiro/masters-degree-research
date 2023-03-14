
import pandas as pd
import numpy as np
import os

import mechanisms

es = [ .01, .1, .5, 1 ] 

runs = 10

df         = pd.read_csv('Datasets/Unicauca-dataset-April-June-2019-Network-flows.csv', sep=';', nrows = None)
#df         = pd.read_csv('Datasets/traffic_table4.csv', sep=';', nrows = None)

col = ['DESTPORT', 'PROTOCOL', 'SERVICE']

df_counts = df.sort_values(['DESTPORT'],ascending=False).groupby(col)['SERVICE'].count().to_csv('counts.csv', sep=';')
df_counts = pd.read_csv('counts.csv', sep=';', nrows = None)
df_counts = df_counts.rename(columns={'SERVICE.1':'COUNT'})

df_port = df_counts.groupby(['DESTPORT', 'PROTOCOL']).sum().reset_index()
df_prot = df['PROTOCOL'].value_counts().rename_axis('PROTOCOL').reset_index(name='COUNT').sort_values(['PROTOCOL'])
df_serv = df['SERVICE'].value_counts().rename_axis('SERVICE').reset_index(name='COUNT').sort_values(['SERVICE'])

col = df_counts.columns

for e in es:
    print('--------- eps ' + str(e) + ' ---------')
    # for r in range(runs):
    #     print('...... run ' + str(r) + ' ......')
    
    df_counts[e] = mechanisms.geometric(df_counts['COUNT'].to_numpy(), e)
    df_port[e]   = mechanisms.geometric(df_port['COUNT'].to_numpy(), e)
    df_prot[e]   = mechanisms.geometric(df_prot['COUNT'].to_numpy(), e)
    df_serv[e]   = mechanisms.geometric(df_serv['COUNT'].to_numpy(), e)

print(df_counts)