import pandas as pd

df = pd.read_csv('Datasets/Unicauca-dataset-April-June-2020-Network-flows_2.csv', sep=';')

df = df.rename(columns={'dst_port': 'DESTPORT', 'proto': 'PROTOCOL', 'web_service': 'SERVICE'})

di = {1: 'ICMP', 
      6: 'TCP',
      17: 'UDP'
      }

df['PROTOCOL'] = df['PROTOCOL'].map(di)

df = df[df['PROTOCOL'] != 'ICMP']

df = df.to_csv('Datasets/Unicauca-dataset-April-June-2020-Network-flows_2.csv', sep=';', index=False)