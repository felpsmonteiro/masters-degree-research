import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import functions as fc

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

y = [60, 30, 9, 1] 
x = ['Netflix', 'AmazonVideo', 'AppleTv', 'Looke']

fig, ax = plt.subplots(figsize =(9, 5))
ax.grid(b = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)

plt.bar(x, y)
plt.xticks(x)
addlabels(x, y)
plt.xlabel('Serviço de Streaming')
plt.ylabel('Acessos')
plt.tight_layout()
plt.show()