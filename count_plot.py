import os
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import functions as fc


ft = 16

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center', fontsize=ft)

y = [60, 30, 9, 1] 
x = ['Netflix', 'AmazonVideo', 'AppleTv', 'Looke']

fig, ax = plt.subplots(figsize =(10, 5))
ax.grid(visible = True, color ='grey',
        linestyle ='-.', linewidth = 0.5,
        alpha = 0.2)

plt.bar(x, y, color=('#1f306e', '#553772', '#8f3b76','#c7417b'))
#plt.bar(x, y)
plt.xticks(x, fontsize=ft-2)
plt.yticks(fontsize=ft-2)
addlabels(x, y)
plt.xlabel('Serviços de Streaming', fontsize=ft+2)
plt.ylabel('Acessos', fontsize=ft+2)
plt.tight_layout()
plt.show()