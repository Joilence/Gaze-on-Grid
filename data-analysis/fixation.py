import math
from statistics import mean

def cal_centroid(x1, y1, x2, y2):
    return [(x1+x2)/2, (y1+y2)/2]

def generate_IVT_fixation(data, v_th, xn='GazeX', yn='GazeY'):
    """
    Gives fixations from data based on IVT

    Args:
        data (pandas.DataFrame): raw data from GazeCloud
        v_th (number): threshold of velocity between points to determine fixation
        xn (str, optional): attribute name of coordinate x. Defaults to 'GazeX'.
        yn (str, optional): attribute name of coordinate y. Defaults to 'GazeY'.

    Returns:
        fixations[fixation]: [description]
    """
    # initialization
    fixations = []
    cur_fixation = {'points': []}
    _in_fixation = False
    start = 0
    ###

    def cal_v(x1, y1, x2, y2, time):
        distance = math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return distance / time

    for i in range(len(data)):
        if (i + 1 == len(data)): break
        cur = data.iloc[i]
        nex = data.iloc[i+1]
        try:
            # if [d, v, t] column is added by preprocessing
            v = v = cur['velocity']
        else:
            v = cal_v(cur[xn], cur[yn], nex[xn], nex[yn], nex['time'] - cur['time'])

        if v < v_th:
            # enter fixation if not in
            if _in_fixation is False:
                start = cur['time']
                _in_fixation = True
            # record fixation
            cur_fixation['points'].append(cur)
        if v > v_th and _in_fixation is True:
            # finish information of fixation
            cur_fixation['points'].append(cur)
            cur_fixation['centroid'] = [mean([p[xn] for p in cur_fixation['points']]),
                                        mean([p[yn] for p in cur_fixation['points']])]
            cur_fixation['duration'] = cur['time'] - start
            fixations.append(cur_fixation)
            # reset
            _in_fixation = False
            cur_fixation = {'points': []}
            start = 0
            
    return fixations