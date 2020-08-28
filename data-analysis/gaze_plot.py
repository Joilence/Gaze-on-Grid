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