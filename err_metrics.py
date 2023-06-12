import numpy as np
from scipy.stats import t

def calculate(error_metric, orig, pert, k, alpha):
    if error_metric == 'mae':
        error = mae(orig, pert)
    
    elif error_metric == 'mre':
        error = mre(orig, pert)
    
    elif error_metric == 'op':
        error = op(orig, pert, k=k)
        
    elif error_metric == 'jaccard':
        error = jaccard_distance_non_zeros(orig, pert, k=k)
    
    elif error_metric == 'ttest':
        error = ttest(orig, pert, alpha)

    return error

# Mean Absolute Error
def mae(orig, pert):       
    error = np.mean( np.abs(orig - pert) )
    return error

# Mean Relative Error
def mre(orig, pert):     
    error = np.mean( np.abs(pert - orig ) / orig  )
    return error

# overlapping percentage
def op(orig, pert, k):
    topk_true = np.argsort(-orig)[:k]            
    topk_pred = np.argsort(-pert)[:k]            
    perc = len(set(topk_true) & set(topk_pred)) / k
    # msgs.log_msg('overlapping percentage = %f' % error )
    return perc

def jaccard_distance_non_zeros(orig, pert, k):
    topk_true = set(np.argsort(-orig)[:k])
    topk_pred = set(np.argsort(-pert)[:k])

    intersection_cardinality = len(topk_true.intersection(topk_pred))
    union_cardinality = len(topk_true.union(topk_pred))
    distance = intersection_cardinality / float(union_cardinality)
    
    return distance

# T-test p-value
def ttest(sample1, sample2, alpha):
    # Cálculo das estatísticas das duas amostras
    n1 = len(sample1)
    n2 = len(sample2)
    mean1 = np.mean(sample1)
    mean2 = np.mean(sample2)
    var1 = np.var(sample1, ddof=1)
    var2 = np.var(sample2, ddof=1)

    # Cálculo do valor crítico de t para um determinado nível de significância (alpha)
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    se = np.sqrt(pooled_var * (1/n1 + 1/n2))
    t_critical = np.abs(np.round(t.ppf(1 - alpha/2, n1 + n2 - 2), 4))

    # Cálculo da estatística de teste
    t_statistic = (mean1 - mean2) / se

    # Verificação se a estatística de teste está na região de rejeição
    if np.abs(t_statistic) > t_critical:
        h0 = print(f'A diferença entre as médias é estatisticamente significativa. -- {t_critical}')
    else:
        h1 = print(f'A diferença entre as médias não é estatisticamente significativa. -- {t_critical}')

    
