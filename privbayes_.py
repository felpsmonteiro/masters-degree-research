
import pandas as pd
import numpy as np
import os


df         = pd.read_csv('Datasets/Unicauca-dataset-April-June-2019-Network-flows.csv', sep=';', nrows = None)
#df         = pd.read_csv('Datasets/traffic_table4.csv', sep=';', nrows = None)


print(df.columns)
# df.groupby(['DESTPORT','SERVICE','PROTOCOL'])['DESTPORT'].count()