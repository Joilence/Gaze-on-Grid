import os
from scipy import stats

def get_participant_names(path):
    names = set()
    for _,_, fns in os.walk(path):
        for fn in fns:
            # print(fn.split('_')[0])
            names.add(fn.split('_')[0])
    return list(names)

def remove_outlier_by_z(data, attr, z_th=3):
    zs = stats.zscore(data[attr])
    outlier = [i for i, z in enumerate(zs) if abs(z) >= 3]
    return data.drop(data.index[outlier])