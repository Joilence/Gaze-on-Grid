import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import numpy as np
from fixation import generate_IVT_fixation

def fixation_based_plot(data, v_th=0.5, d_th=300, xn='GazeX', yn='GazeY', background=None):
    # plot based on fixation
    fixations = generate_IVT_fixation(data=data, v_th=v_th, d_th=d_th, xn=xn, yn=yn)
    fixations_points = np.array([f['centroid'] for f in fixations])
    durations = [f['duration'] for f in fixations]

    if not fixations:
        print('No fixation detected.')
        return plt.axes()

    plt.axis('off')

    # fixation point
    ax = sns.scatterplot(x=fixations_points[:, 0], y=fixations_points[:, 1],
                    size=300, sizes=(100,200),
                    hue=durations, alpha=0.8,
                    legend=False)

    # background image
    if background is not None:
        plt.imshow(background, zorder=0, alpha=0.5,
                aspect=ax.get_aspect(),
                extent=ax.get_xlim() + ax.get_ylim())

    # draw grid
    (x_min, x_max) = ax.get_xlim()
    (y_min, y_max) = ax.get_ylim()
    # - horizontal
    hlines_y = [y_min, (y_min + y_max)/2, y_max]
    plt.hlines(hlines_y, xmin=x_min, xmax=x_max,
            zorder=1, alpha=0.3)
    # - vertical
    n = (x_max - x_min) / 3
    plt.vlines([round(x_min + i*n, 4) for i in range(4)],
            ymin=y_min, ymax=y_max,
            zorder=1, alpha=0.3)

    # draw scan path
    arrow_style = mpatches.ArrowStyle.CurveFilledB(head_length=10, head_width=5)
    for i, f in enumerate(fixations_points):
        # if i == 3: break
        if i + 1 == len(fixations): break
        nex = fixations_points[i+1]
        cur = fixations_points[i]
        arrow = mpatches.FancyArrowPatch((cur[0], cur[1]), (nex[0], nex[1]), arrowstyle=arrow_style, alpha=0.5)
        ax.add_patch(arrow)
        # annotation of order
        x_anno = (cur[0] + nex[0])/2
        y_anno = (cur[1] + nex[1])/2
        b_props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        plt.text(x=x_anno, y=y_anno, s=i+1, backgroundcolor='white', bbox=b_props, size=7)
    
    return ax

def grid_based_plot(data, v_th=0.5, d_th=300, xn='GazeX', yn='GazeY', background=None):
    # plot based on fixation
    fixations = generate_IVT_fixation(data=data, v_th=v_th, d_th=d_th, xn=xn, yn=yn)
    fixations_points = np.array([f['centroid'] for f in fixations])
    durations = [f['duration'] for f in fixations]


    if not fixations:
        print('No fixation detected.')
        return plt.axes()

    # plt.axis('off')

    # fixation point
    ax = sns.scatterplot(x=fixations_points[:, 0], y=fixations_points[:, 1],
                    s=30, alpha=0.8, legend=False, zorder=9)

    # background image
    if background is not None:
        plt.imshow(background, zorder=0, alpha=0.5,
                aspect=ax.get_aspect(),
                extent=ax.get_xlim() + ax.get_ylim())

    # draw grid
    (x_min, x_max) = ax.get_xlim()
    (y_min, y_max) = ax.get_ylim()
    # - horizontal
    hlines_y = [y_min, (y_min + y_max)/2, y_max]
    plt.hlines(hlines_y, xmin=x_min, xmax=x_max,
            zorder=1, alpha=0.3)
    # - vertical
    n = (x_max - x_min) / 3
    plt.vlines([round(x_min + i*n, 4) for i in range(4)],
            ymin=y_min, ymax=y_max,
            zorder=1, alpha=0.3)

    # grid from 't'op to 'b'ottom, 'l'eft to 'r'ight
    grid = {'tl':{'pos': [0, 0], 'count': 0, 'time_sum': 0},
            'tm':{'pos': [0, 0], 'count': 0, 'time_sum': 0},
            'tr':{'pos': [0, 0], 'count': 0, 'time_sum': 0},
            'bl':{'pos': [0, 0], 'count': 0, 'time_sum': 0},
            'bm':{'pos': [0, 0], 'count': 0, 'time_sum': 0},
            'br':{'pos': [0, 0], 'count': 0, 'time_sum': 0}}
    
    # calculate centroid of each rectangle in the grid
    x_n = (x_max - x_min) / 6
    y_n = (y_max - y_min) / 4
    ########### ALERT: here depends on coordinate. but no actual influence. ###########
    for key in grid.keys():
        # left, middle and right
        if 'l' in key: grid[key]['pos'][0] = x_min + x_n * 1
        if 'm' in key: grid[key]['pos'][0] = x_min + x_n * 3
        if 'r' in key: grid[key]['pos'][0] = x_min + x_n * 5
        # top and bottom
        if 't' in key: grid[key]['pos'][1] = y_min + y_n * 3
        if 'b' in key: grid[key]['pos'][1] = y_min + y_n * 1
    
    def nearest_in_grid(grid, point):
        #TODO: another method: just find a grid that distance to its centroid lower than half of the edge len
        d = float('inf')
        rect = ''
        # print('point: ', point)
        for key in grid.keys():
            man_dis = abs(grid[key]['pos'][0] - point[0]) + abs(grid[key]['pos'][1] - point[1])
            # print('key: ', key, ', ', man_dis, 'now_d:', d, 'now_key', key, 'now_rect', rect)
            if man_dis < d:
                d = man_dis
                rect = key
        return rect
    
    # fit fixation into rectangles in grid
    fixation_rects = []
    for f in fixations:
        rect = nearest_in_grid(grid, f['centroid'])
        fixation_rects.append(rect)
        grid[rect]['count'] = grid[rect]['count'] + 1
        grid[rect]['time_sum'] = grid[rect]['time_sum'] + f['duration']
    # print(fixation_rects)
    
    
    [count * 10 * (-1)**count for count in range(10)]

    # draw scan path
    arrow_style = mpatches.ArrowStyle.CurveFilledB(head_length=10, head_width=5)
    if (False):
        # - grid based
        for i, rect in enumerate(fixation_rects):
            if i + 1 == len(fixation_rects): break

            nex_rect = fixation_rects[i+1]
            cur = grid[rect]['pos']
            nex = grid[nex_rect]['pos']
            # print('cur: ', cur, 'nex: ', nex)

            arrow = mpatches.FancyArrowPatch((cur[0], cur[1]), (nex[0], nex[1]), arrowstyle=arrow_style, alpha=0.5)
            ax.add_patch(arrow)
            # annotation of order
            x_anno = (cur[0] + nex[0])/2
            y_anno = (cur[1] + nex[1])/2
            b_props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            plt.text(x=x_anno, y=y_anno, s=i+1, backgroundcolor='white', bbox=b_props, size=7)
    else:
        # - fixation based
        for i, f in enumerate(fixations_points):
            # if i == 3: break
            if i + 1 == len(fixations): break
            nex = fixations_points[i+1]
            cur = fixations_points[i]
            arrow = mpatches.FancyArrowPatch((cur[0], cur[1]), (nex[0], nex[1]), arrowstyle=arrow_style, alpha=0.3)
            ax.add_patch(arrow)
            # annotation of order
            x_anno = (cur[0] + nex[0])/2
            y_anno = (cur[1] + nex[1])/2
            b_props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            plt.text(x=x_anno, y=y_anno, s=i+1, backgroundcolor='white', bbox=b_props, size=7, zorder=10, alpha=0.3)

    sns.scatterplot(x=[grid[key]['pos'][0] for key in grid.keys()],
                    y=[grid[key]['pos'][1] for key in grid.keys()],
                    size=[grid[key]['count'] for key in grid.keys()], sizes=(100, 1000),
                    alpha=0.8, legend=False)
    
    return ax, grid_based_plot