import numpy as np

def geometric(arr, eps, sensitivity=1):
    p = 1 - np.exp(-eps/sensitivity) 
    noise = np.random.geometric(p, len(arr)) - np.random.geometric(p, len(arr))
    arr_noisy = arr + noise
    return np.array(arr_noisy)

def log_laplace(arr, eps, sensitivity=1):
    lap = np.random.laplace(loc=0, scale=sensitivity/eps, size=len(arr))
    noisy_arr = np.around(np.clip(arr * np.exp(lap), 1, max(arr))).astype(int)  # https://arxiv.org/pdf/2101.02957.pdf
    return np.array(noisy_arr)

def post_processing(arr_orig, min_value=1):
    arr = np.array(arr_orig).astype('int')
    desired_sum = np.sum(arr_orig)

    if desired_sum < len(arr)*min_value:
        return (np.ones(len(arr))*min_value).astype('int')

    arr = np.clip(arr, min_value, np.max(arr))

    exceding_units = int(np.sum(arr) -desired_sum)

    if exceding_units > 0:
        sign = -1
    elif exceding_units < 0:
        sign = 1
    else:
        sign = 0

    exceding_units = np.abs(exceding_units)

    if sign == -1:

        while exceding_units > len(np.where(arr > min_value)[0]):
            exceding_units -= len(arr[np.where(arr > min_value)[0]])
            arr[np.where(arr > min_value)[0]] += sign*1
        if exceding_units > 0:
            p = np.ones(len(arr)).astype('int')
            p[np.where(arr <= min_value)[0]] = 0
            prob = p/np.sum(p)
            idx_to_decrease_1 = np.random.choice(len(arr), exceding_units, replace=False, p=prob)
            arr[idx_to_decrease_1] += sign*1
    elif sign == 1:
        while exceding_units > len(arr):
            exceding_units -= len(arr)
            arr += sign*1
        if exceding_units > 0:
            idx_to_increase_1 = np.random.choice(len(arr), exceding_units, replace=False)
            arr[idx_to_increase_1] += sign*1
    
    if np.sum(arr) != desired_sum and len(np.where(arr < min_value)[0]) > 0:
        print("error in min l2 method")

    return arr