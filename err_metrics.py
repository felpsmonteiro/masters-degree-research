import numpy as np

def calculate(error_metric, orig, pert, k=2):
    if error_metric == 'mae':
        error = mae(orig, pert)
    elif error_metric == 'mre':
        error = mre(orig, pert)
    elif error_metric == 'op':
        error = op(orig, pert, k=k)
    elif error_metric == 'jaccard':
        error = jaccard_distance_non_zeros(orig, pert, k=k)
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