
import pandas as pd
import numpy as np
import os

import functions as fc





eps = [0.01, 0.05, .1, .5, 1]
#eps = [0.01]
#rowstoread = 500000

#Dataset Cleanning/Adjustments

traf_df         = pd.read_csv('Unicauca-dataset-April-June-2019-Network-flows.csv', sep=';', nrows = None)
#traf_df         = pd.read_csv('traffic_table4.csv', sep=';', nrows = None)
# 
traf_df_priv    = traf_df[['DESTPORT', 'PROTOCOL', 'SERVICE']]

traf_df_priv['INDEX_COLUMN'] = traf_df_priv.index
traf_df_priv.reset_index
traf_df_priv.to_csv('privBayesDataFrame_Local.csv')

thre_shold = int(len(traf_df_priv['SERVICE'].unique()) + 10)
cat_Attribute = {'DESTPORT': True, 'PROTOCOL': True, 'SERVICE': True}
candidateKeys = {'INDEX_COLUMN': True}

for e in eps:
    for n in range(10):
        fc.syntheticData('Kaggle', 'privBayesDataFrame_Local.csv', thre_shold, cat_Attribute, candidateKeys, e, n, len(traf_df_priv), 2)

