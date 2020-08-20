import math

def calculate_dist_and_veloc(data, xn='GazeX', yn='GazeY'):
    """
    Calculate columns of distance, velocity and time passed between points.

    Args:
        data (pandas.DataFrame): raw data from GazeCloud
        xn (str, optional): attribute name of coordinate x. Defaults to 'GazeX'.
        yn (str, optional): attribute name of coordinate y. Defaults to 'GazeY'.

    Returns:
        d, v, t (list, list, list): lists of distance, velocity and time passed
    """

    # initialization
    d = []
    t = []
    v = []
    ###

    for i in range(len(data)):
        if i + 1 == len(data):
            d.append(0)
            t.append(0)
            v.append(0)
            break

        cur = data.iloc[i]
        nex = data.iloc[i+1]
        d.append(math.sqrt((cur[xn]-nex[xn])**2 + (cur[yn]-nex[yn])**2))
        t.append(nex['time'] - cur['time'])
        v.append(d[i] / t[i])
    return d, v, t