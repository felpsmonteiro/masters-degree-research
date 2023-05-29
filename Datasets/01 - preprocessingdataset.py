import pandas as pd


df = pd.read_csv('Datasets/Copy of Darknet.csv', sep=';')
df['SERVICE'] = df['Label'].astype(str) + '_' + df['Label.1'].astype(str)

df = df.rename(columns={'Dst Port': 'DESTPORT', 'Protocol': 'PROTOCOL'})
# df = df.rename(columns={'dst_port': 'DESTPORT', 'proto': 'PROTOCOL', 'web_service': 'SERVICE'})

di = {0: 'HOPOPT', 
      6: 'TCP',
      17: 'UDP'
      }

df['PROTOCOL'] = df['PROTOCOL'].map(di)

df = df[df['PROTOCOL'] != 'HOPOPT']

df = df.to_csv('Datasets/Canadian-Institute-for-Cybersecurity.csv', sep=';', index=False)