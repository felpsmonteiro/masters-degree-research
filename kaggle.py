import math
import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns

import functions as fc

sensitivity, eps = 1, [0.01, 0.05, .1, .5, 1]
rowstoread = None
rangetimes = 10

#Dataset Cleanning/Adjustments
traf_df                     = pd.read_csv('Unicauca-dataset-April-June-2019-Network-flows.csv', sep=';', nrows=None)
traf_df["DESTPORT"]         = pd.to_numeric(traf_df["DESTPORT"])
protocol, service, ports    = traf_df['PROTOCOL'].unique(), np.array(traf_df['SERVICE'].unique()), np.array(traf_df['DESTPORT'].unique())

#Count by tree level;
prot_count, serv_count, ports_count = fc.Count(protocol, traf_df, "PROTOCOL"), fc.Count(service, traf_df, "SERVICE"), fc.Count(ports, traf_df, "DESTPORT")
#l_count                             = [ports_count, serv_count]

#Count by New Dataset (PrivBayes);
p_c, p_s, prot_c       = [], [], []
for e in eps:
    count_p, count_s, count_pr        = [], [], []
    
    for path, currentDirectory, files in os.walk(f'Kaggle/{e}'):
        for file in files:
            if file.endswith('.csv'):
                print(f'FOR EPSLON: {e}: Arquivo: {file}')
                traf_d                              = pd.read_csv(f'Kaggle/{e}/{file}', sep=',', nrows = None)
                
                traf_d["DESTPORT"]                  = pd.to_numeric(traf_d["DESTPORT"])
                prot, ser, po                       = np.array(traf_d['PROTOCOL'].unique()), np.array(traf_d['SERVICE'].unique()), np.array(traf_d['DESTPORT'].unique())
                
                p_count, s_count, pr_count          = [], [], []
                                 
                traf_d_pt = traf_d.groupby('DESTPORT').count()['SERVICE']
                traf_d_s = traf_d.groupby('SERVICE').count()['DESTPORT']
                traf_d_p = traf_d.groupby('PROTOCOL').count()['DESTPORT']
                                
                for p_ in ports:
                    p_count.append(traf_d_pt[traf_d_pt.index == p_].item())
                    
                for s in service:
                    s_count.append(traf_d_s[traf_d_s.index == s].item())
                    
                for p in protocol:
                    pr_count.append(traf_d_p[traf_d_p.index == p].item())
                #l_count_                =  [p_count, s_count]
          
                count_p.append(p_count), count_s.append(s_count), count_pr.append(pr_count)

    p_c.append(count_p), p_s.append(count_s), prot_c.append(count_pr)


#BASELINE # GM, MAE, MRE [Ports, Service] [Protocol] - EPS/3 APPROACH
mae_ports, mae_service, mre_ports, mre_service, level_noisy_p, level_noisy_s        = [], [], [], [], [], []
mae_prot, mre_prot, level_noisy_prot                                                = [], [], []

for e in range(len(eps)):
    
    mae_p, mae_s, mre_p, mre_s,     = [], [], [], []
    mae_l_prot, mre_l_prot          = [], []
    
    level_noisy_p.append([fc.Geometric_Mechanism(ports_count, eps[e]/3, sensitivity) for i in range(rangetimes)])
    level_noisy_s.append([fc.Geometric_Mechanism(serv_count, eps[e]/3, sensitivity) for i in range(rangetimes)])
    level_noisy_prot.append([fc.Geometric_Mechanism(prot_count, eps[e]/3, sensitivity) for i in range(rangetimes)]) 
        
    for at in range(rangetimes):
 
        mae_p.append([fc.mae(ports_count[lv], level_noisy_p[e][at][lv]) for lv in range(len(ports_count))])
        mae_s.append([fc.mae(serv_count[lv], level_noisy_s[e][at][lv]) for lv in range(len(serv_count))])
        
        mre_p.append([fc.mre(ports_count[lv], level_noisy_p[e][at][lv]) for lv in range(len(ports_count))])
        mre_s.append([fc.mre(serv_count[lv], level_noisy_s[e][at][lv]) for lv in range(len(serv_count))])
        
    mae_ports.append(mae_p), mae_service.append(mae_s), mre_ports.append(mre_p), mre_service.append(mre_s)
    
    for at in range(rangetimes):

        mae_l_prot.append([fc.mae(prot_count[lv], level_noisy_prot[e][at][lv]) for lv in range(len(prot_count))])
        mre_l_prot.append([fc.mre(prot_count[lv], level_noisy_prot[e][at][lv]) for lv in range(len(prot_count))])
        
    mae_prot.append(mae_l_prot), mre_prot.append(mre_l_prot)
    
#Mean of Errors - MAE, MRE
#mean_mae, mean_mre = np.mean(np.array(mae), axis=1), np.mean(np.array(mre), axis=1)
# mean_mae_pts, mean_mae_svc, mean_mre_pts, mean_mre_svc = np.mean(np.array(mae_ports), axis=1), np.mean(np.array(mae_service), axis=1), np.mean(np.array(mre_ports), axis=1), np.mean(np.array(mre_service), axis=1)
#mean_mae_prot, mean_mre_prot = np.sum(np.mean(np.array(mae_prot), axis=1)), np.sum(np.mean(np.array(mre_prot), axis=1))

mean_mae_pts, mean_mae_svc, mean_mre_pts, mean_mre_svc = [np.mean(mae_ports[i]) for i in range(len(mae_ports))], [np.mean(mae_service[i]) for i in range(len(mae_service))], [np.mean(mre_ports[i]) for i in range(len(mre_ports))], [np.mean(mre_service[i]) for i in range(len(mre_service))]
mean_mae_prot, mean_mre_prot = [np.mean(mae_prot[i]) for i in range(len(mae_prot))], [np.mean(mre_prot[i]) for i in range(len(mre_prot))]

# GM, MAE, MRE [Ports, Service] [Protocol] - EPS Full
# mae_apr, mre_apr, level_noisy_apr                   = [], [], []
# mae_prot_apr, mre_prot_apr, level_noisy_prot_apr    = [], [], []

mae_p_apr, mae_s_apr, mre_p_apr, mre_s_apr, level_noisy_p_apr, level_noisy_s_apr        = [], [], [], [], [], []
mae_prot_apr, mre_prot_apr, level_noisy_prot_apr    = [], [], []

mae_apr_p_clip, mae_apr_s_clip, mre_apr_p_clip, mre_apr_s_clip                   = [], [], [], []
mae_prot_apr_clip, mre_prot_apr_clip                                             = [], []

mae_apr_p_priv, mae_apr_s_priv, mre_apr_p_priv,  mre_apr_s_priv                  = [], [], [], []
mae_prot_apr_priv, mre_prot_apr_priv                                             = [], []

mae_apr_p_lap, mae_apr_s_lap, mre_apr_p_lap, mre_apr_s_lap, level_noisy_p_lap, level_noisy_s_lap                        = [], [], [], [], [], []
mae_prot_apr_lap, mre_prot_apr_lap, level_noisy_prot_lap         = [], [], []

for e in range(len(eps)):
    # mae_l_apr, mre_l_apr, mae_l_apr_clip, mre_l_apr_clip, mae_l_apr_priv, mre_l_apr_priv, mae_l_lap, mre_l_lap            = [], [], [], [], [], [], [], []
    # mae_l_prot_apr, mre_l_prot_apr, mae_l_prot_apr_clip, mre_l_prot_apr_clip, mae_l_prot_apr_priv, mre_l_prot_apr_priv, mae_l_prot_lap, mre_l_prot_lap  = [], [], [], [], [],[], [], []
    
    mae_l_p_apr, mae_l_s_apr, mae_l_apr_p_clip, mae_l_apr_s_clip, mae_l_apr_p_priv, mae_l_apr_s_priv, mae_l_p_lap, mae_l_s_lap                          = [], [], [], [], [], [], [], []
    mre_l_p_apr, mre_l_s_apr, mre_l_apr_p_clip, mre_l_apr_s_clip, mre_l_apr_p_priv, mre_l_apr_s_priv, mre_l_p_lap, mre_l_s_lap                          = [], [], [], [], [], [], [], []
    mae_l_prot_apr, mre_l_prot_apr, mae_l_prot_apr_clip, mre_l_prot_apr_clip, mae_l_prot_apr_priv, mre_l_prot_apr_priv, mae_l_prot_lap, mre_l_prot_lap  = [], [], [], [], [],[], [], []
   
    level_noisy_p_apr.append([fc.Geometric_Mechanism(ports_count, eps[e], sensitivity) for i in range(rangetimes)])
    level_noisy_s_apr.append([fc.Geometric_Mechanism(serv_count, eps[e], sensitivity) for i in range(rangetimes)])
    level_noisy_prot_apr.append([fc.Geometric_Mechanism(prot_count, eps[e], sensitivity) for i in range(rangetimes)])

    level_noisy_p_lap.append([fc.log_laplace_mechanism(ports_count, eps[e], sensitivity) for i in range(rangetimes)])
    level_noisy_s_lap.append([fc.log_laplace_mechanism(serv_count, eps[e], sensitivity) for i in range(rangetimes)])
    level_noisy_prot_lap.append([fc.log_laplace_mechanism(prot_count, eps[e], sensitivity) for i in range(rangetimes)])

    for at in range(rangetimes):
 
        mae_l_p_apr.append([fc.mae(ports_count[lv], level_noisy_p_apr[e][at][lv]) for lv in range(len(ports_count))])
        mae_l_s_apr.append([fc.mae(serv_count[lv], level_noisy_s_apr[e][at][lv]) for lv in range(len(serv_count))])
        
        mre_l_p_apr.append([fc.mre(ports_count[lv], level_noisy_p_apr[e][at][lv]) for lv in range(len(ports_count))])
        mre_l_s_apr.append([fc.mre(serv_count[lv], level_noisy_s_apr[e][at][lv]) for lv in range(len(serv_count))])
        
        mae_l_apr_p_clip.append([fc.mae(ports_count[lv], np.clip(level_noisy_p_apr[e][at][lv], 1, None)) for lv in range(len(ports_count))])
        mae_l_apr_s_clip.append([fc.mae(serv_count[lv], np.clip(level_noisy_s_apr[e][at][lv], 1, None)) for lv in range(len(serv_count))])
        
        mre_l_apr_p_clip.append([fc.mre(ports_count[lv], np.clip(level_noisy_p_apr[e][at][lv], 1, None)) for lv in range(len(ports_count))])
        mre_l_apr_s_clip.append([fc.mre(serv_count[lv], np.clip(level_noisy_s_apr[e][at][lv], 1, None)) for lv in range(len(serv_count))])
      
        mae_l_apr_p_priv.append([fc.mae(ports_count[lv], p_c[e][at][lv]) for lv in range(len(ports_count))])
        mae_l_apr_s_priv.append([fc.mae(serv_count[lv], p_s[e][at][lv]) for lv in range(len(serv_count))])
        
        mre_l_apr_p_priv.append([fc.mre(ports_count[lv], p_c[e][at][lv]) for lv in range(len(ports_count))])
        mre_l_apr_s_priv.append([fc.mre(serv_count[lv], p_s[e][at][lv]) for lv in range(len(serv_count))])
        
        mae_l_p_lap.append([fc.mae(ports_count[lv], level_noisy_p_lap[e][at][lv]) for lv in range(len(ports_count))])
        mae_l_s_lap.append([fc.mae(serv_count[lv], level_noisy_s_lap[e][at][lv]) for lv in range(len(serv_count))])
        
        mre_l_p_lap.append([fc.mre(ports_count[lv], level_noisy_p_lap[e][at][lv]) for lv in range(len(ports_count))])
        mre_l_s_lap.append([fc.mre(serv_count[lv], level_noisy_s_lap[e][at][lv]) for lv in range(len(serv_count))])

        
    mae_p_apr.append(mae_l_p_apr), mre_p_apr.append(mre_l_p_apr)
    mae_s_apr.append(mae_l_s_apr), mre_s_apr.append(mre_l_s_apr)
    
    mae_apr_p_clip.append(mae_l_apr_p_clip), mre_apr_p_clip.append(mre_l_apr_p_clip)
    mae_apr_s_clip.append(mae_l_apr_s_clip), mre_apr_s_clip.append(mre_l_apr_s_clip)
    
    mae_apr_p_priv.append(mae_l_apr_p_priv), mre_apr_p_priv.append(mre_l_apr_p_priv)
    mae_apr_s_priv.append(mae_l_apr_s_priv), mre_apr_s_priv.append(mre_l_apr_s_priv)
    
    mae_apr_p_lap.append(mae_l_p_lap), mre_apr_p_lap.append(mre_l_p_lap)
    mae_apr_s_lap.append(mae_l_s_lap), mre_apr_s_lap.append(mre_l_s_lap)
    
    for at in range(rangetimes):

        mae_l_prot_apr.append([fc.mae(prot_count[lv], level_noisy_prot_apr[e][at][lv]) for lv in range(len(prot_count))])
        mre_l_prot_apr.append([fc.mre(prot_count[lv], level_noisy_prot_apr[e][at][lv]) for lv in range(len(prot_count))])
        
        mae_l_prot_apr_clip.append([fc.mae(prot_count[lv], np.clip(level_noisy_prot_apr[e][at][lv], 1, None)) for lv in range(len(prot_count))])
        mre_l_prot_apr_clip.append([fc.mre(prot_count[lv], np.clip(level_noisy_prot_apr[e][at][lv], 1, None)) for lv in range(len(prot_count))])
        
        mae_l_prot_apr_priv.append([fc.mae(prot_count[lv], prot_c[e][lv]) for lv in range(len(prot_count))])
        mre_l_prot_apr_priv.append([fc.mre(prot_count[lv], prot_c[e][lv]) for lv in range(len(prot_count))])
        
        mae_l_prot_lap.append([fc.mae(prot_count[lv], level_noisy_prot_lap[e][at][lv]) for lv in range(len(prot_count))])
        mre_l_prot_lap.append([fc.mre(prot_count[lv], level_noisy_prot_lap[e][at][lv]) for lv in range(len(prot_count))])        
    
    mae_prot_apr.append(mae_l_prot_apr), mre_prot_apr.append(mre_l_prot_apr)
    mae_prot_apr_clip.append(mae_l_prot_apr_clip), mre_prot_apr_clip.append(mre_l_prot_apr_clip)
    mae_prot_apr_priv.append(mae_l_prot_apr_priv), mre_prot_apr_priv.append(mre_l_prot_apr_priv)
    mae_prot_apr_lap.append(mae_l_prot_lap), mre_prot_apr_lap.append(mre_l_prot_lap)

mean_mae_p_apr, mean_mre_p_apr                     = [np.mean(mae_p_apr[i]) for i in range(len(mae_p_apr))], [np.mean(mre_p_apr[i]) for i in range(len(mre_p_apr))]
mean_mae_s_apr, mean_mre_s_apr                     = [np.mean(mae_s_apr[i]) for i in range(len(mae_s_apr))], [np.mean(mre_s_apr[i]) for i in range(len(mre_s_apr))]
mean_mae_prot_apr, mean_mre_prot_apr               = np.sum(np.mean(np.array(mae_prot_apr), axis=1), axis=1), np.sum(np.mean(np.array(mre_prot_apr), axis=1), axis=1)

mean_mae_apr_p_clip, mean_mre_apr_p_clip           = [np.mean(mae_apr_p_clip[i]) for i in range(len(mae_apr_p_clip))], [np.mean(mre_apr_p_clip[i]) for i in range(len(mre_apr_p_clip))]
mean_mae_apr_s_clip, mean_mre_apr_s_clip           = [np.mean(mae_apr_s_clip[i]) for i in range(len(mae_apr_s_clip))], [np.mean(mre_apr_s_clip[i]) for i in range(len(mre_apr_s_clip))]
mean_mae_prot_apr_clip, mean_mre_prot_apr_clip     = np.sum(np.mean(np.array(mae_prot_apr_clip), axis=1), axis=1), np.sum(np.mean(np.array(mre_prot_apr_clip), axis=1), axis=1)

mean_mae_apr_p_priv, mean_mre_apr_p_priv           = [np.mean(mae_apr_p_priv[i]) for i in range(len(mae_apr_p_priv))], [np.mean(mre_apr_p_priv[i]) for i in range(len(mre_apr_p_priv))]
mean_mae_apr_s_priv, mean_mre_apr_s_priv           = [np.mean(mae_apr_s_priv[i]) for i in range(len(mae_apr_s_priv))], [np.mean(mre_apr_s_priv[i]) for i in range(len(mre_apr_s_priv))]
mean_mae_prot_apr_priv, mean_mre_prot_apr_priv     = np.sum(np.mean(np.array(mae_prot_apr_priv), axis=1), axis=1), np.sum(np.mean(np.array(mre_prot_apr_priv), axis=1), axis=1)

mean_mae_apr_p_lap, mean_mre_apr_p_lap             = [np.mean(mae_apr_p_lap[i]) for i in range(len(mae_apr_p_lap))], [np.mean(mre_apr_p_lap[i]) for i in range(len(mre_apr_p_lap))]
mean_mae_apr_s_lap, mean_mre_apr_s_lap             = [np.mean(mae_apr_s_lap[i]) for i in range(len(mae_apr_s_lap))], [np.mean(mre_apr_s_lap[i]) for i in range(len(mre_apr_s_lap))]
mean_mae_prot_apr_lap, mean_mre_prot_apr_lap       = np.sum(np.mean(np.array(mae_prot_apr_lap), axis=1), axis=1), np.sum(np.mean(np.array(mre_prot_apr_lap), axis=1), axis=1)

##############################################################################################################
##### MRE #####

#Ports Baseline x Approach
epsilons = eps                    # privacy budgets
error_metr = 'mre'                           # mre ou mae, depende do que tu tá medindo
path = "Images/ports_mre_gm_results2.png"                # path de onde tu quer salvar a imagem
legends = ['Mecanismo Geométrico', 'Abordagem Hierárquica', '2° Pós-Processamento', 'PrivBayes', 'LogLaplace']     # primeira abordagem: mec. geometrico
y = []                                       # erros de diferentes abordagens
y.append(mean_mre_pts)                           # erros do geometrico, retornados pela função mre ou mae
y.append(mean_mre_p_apr)
y.append(mean_mre_apr_p_clip)
y.append(mean_mre_apr_p_priv)
y.append(mean_mre_apr_p_lap)
print(y)
fc.line_plot(epsilons, y, xlabel='$\epsilon$',
    ylabel= error_metr, ylog=True, line_legends=legends, title="Erro Relativo Médio - Portas", 
    colors = ['#4ECE00', '#360CE8', '#FFFF00', '#F01F0F', '#AF10E0'], path = path)

#Services Baseline x Approach)
epsilons = eps                    # privacy budgets
error_metr = 'mre'                           # mre ou mae, depende do que tu tá medindo
path = "Images/services_mre_gm_results2.png"                # path de onde tu quer salvar a imagem
legends = ['Mecanismo Geométrico', 'Abordagem Hierárquica', '2° Pós-Processamento', 'PrivBayes', 'LogLaplace']     # primeira abordagem: mec. geometrico
y = []                                       # erros de diferentes abordagens
y.append(mean_mre_svc)                           # erros do geometrico, retornados pela função mre ou mae
y.append(mean_mre_s_apr)
y.append(mean_mre_apr_s_clip)
y.append(mean_mre_apr_s_priv)
y.append(mean_mre_apr_s_lap)
print(y)
fc.line_plot(epsilons, y, xlabel='$\epsilon$',
    ylabel= error_metr, ylog=True, line_legends=legends, title="Erro Relativo Médio - Serviços", 
    colors = ['#4ECE00', '#360CE8', '#FFFF00', '#F01F0F', '#AF10E0'], path = path)

#Protocols Baseline x Approach
epsilons = eps                    # privacy budgets
error_metr = 'mre'                           # mre ou mae, depende do que tu tá medindo
path = "Images/protocols_mre_gm_results2.png"               # path de onde tu quer salvar a imagem
legends = ['Mecanismo Geométrico', 'Abordagem Hierárquica', '2° Pós-Processamento', 'PrivBayes', 'LogLaplace']     # primeira abordagem: mec. geometrico
y = []                                       # erros de diferentes abordagens
y.append(mean_mre_prot)                           # erros do geometrico, retornados pela função mre ou mae
y.append(mean_mre_prot_apr)
y.append(mean_mre_prot_apr_clip)
y.append(mean_mre_prot_apr_priv)
y.append(mean_mre_prot_apr_lap)
print(y)
fc.line_plot(epsilons, y, xlabel='$\epsilon$',
    ylabel= error_metr, ylog=True, line_legends=legends, title="Erro Relativo Médio - Protocolos", 
    colors = ['#4ECE00', '#360CE8', '#FFFF00', '#F01F0F', '#AF10E0'], path = path)

#### MAE #####
#Ports Baseline x Approach
epsilons = eps                    # privacy budgets
error_metr = 'mae'                           # mre ou mae, depende do que tu tá medindo
path = "Images/ports_mae_gm_results2.png"                # path de onde tu quer salvar a imagem
legends = ['Mecanismo Geométrico', 'Abordagem Hierárquica', '2° Pós-Processamento', 'PrivBayes', 'LogLaplace']     # primeira abordagem: mec. geometrico
y = []                                       # erros de diferentes abordagens
y.append(mean_mae_pts)                           # erros do geometrico, retornados pela função mre ou mae
y.append(mean_mae_p_apr)
y.append(mean_mae_apr_p_clip)
y.append(mean_mae_apr_p_priv)
y.append(mean_mae_apr_p_lap)
print(y)
fc.line_plot(epsilons, y, xlabel='$\epsilon$',
    ylabel= error_metr, ylog=True, line_legends=legends, title="Erro Relativo Absoluto - Portas", 
    colors = ['#4ECE00', '#360CE8', '#FFFF00', '#F01F0F', '#AF10E0'], path = path) 

#Services Baseline x Approach
epsilons = eps                    # privacy budgets
error_metr = 'mae'                           # mre ou mae, depende do que tu tá medindo
path = "Images/services_mae_gm_results2.png"                # path de onde tu quer salvar a imagem
legends = ['Mecanismo Geométrico', 'Abordagem Hierárquica', '2° Pós-Processamento', 'PrivBayes', 'LogLaplace']     # primeira abordagem: mec. geometrico
y = []                                       # erros de diferentes abordagens
y.append(mean_mae_pts)                           # erros do geometrico, retornados pela função mre ou mae
y.append(mean_mae_s_apr)
y.append(mean_mae_apr_s_clip)
y.append(mean_mae_apr_s_priv)
y.append(mean_mae_apr_s_lap)
print(y)
fc.line_plot(epsilons, y, xlabel='$\epsilon$',
    ylabel= error_metr, ylog=True, line_legends=legends, title="Erro Relativo Absoluto - Serviços", 
    colors = ['#4ECE00', '#360CE8', '#FFFF00', '#F01F0F', '#AF10E0'], path = path)

#Protocols Baseline x Approach
epsilons = eps                    # privacy budgets
error_metr = 'mae'                           # mre ou mae, depende do que tu tá medindo
path = "Images/protocols_mae_gm_results2.png"                # path de onde tu quer salvar a imagem
legends = ['Mecanismo Geométrico', 'Abordagem Hierárquica', '2° Pós-Processamento', 'PrivBayes', 'LogLaplace']     # primeira abordagem: mec. geometrico
y = []                                       # erros de diferentes abordagens
y.append(mean_mae_prot)                           # erros do geometrico, retornados pela função mre ou mae
y.append(mean_mae_prot_apr)
y.append(mean_mae_prot_apr_clip)
y.append(mean_mae_prot_apr_priv)
y.append(mean_mae_prot_apr_lap)
print(y)
fc.line_plot(epsilons, y, xlabel='$\epsilon$',
    ylabel= error_metr, ylog=True, line_legends=legends, title="Erro Relativo Absoluto - Protocol", 
    colors = ['#4ECE00', '#360CE8', '#FFFF00', '#F01F0F', '#AF10E0'], path = path)