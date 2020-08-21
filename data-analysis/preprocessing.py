from scipy import stats

def remove_outlier_by_z(data, attr, z_th=3):
    zs = stats.zscore(data[attr])
    outlier = [i for i, z in enumerate(zs) if abs(z) >= 3]
    return data.drop(outlier)