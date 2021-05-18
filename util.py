import time
import numpy as np

from config import *
from operator import itemgetter
from tqdm import tqdm


###################################

# https://stackoverflow.com/questions/6646371/detect-which-image-is-sharper
def compute_contrast(img):
    dx = np.diff(img)[1:, :] # remove the first row
    dy = np.diff(img, axis=0)[:, 1:] # remove the first column
    dnorm = np.sqrt(dx**2 + dy**2)
    sharpness = np.average(dnorm)
    return sharpness

###################################

def find_knee(x, y):
    knees = []
    prev_curve = float('-inf')
    for i in range(len(x)-1):
        curve = y[i+1] - y[i]
        # A curve is a contender when it was previously increasing in sharpness
        # (right-to-left in the plot) but is currently increasing less than before
        if curve < prev_curve:
            knees.append((x[i], prev_curve - curve))
        prev_curve = curve
    
    # Compute best knee
    if len(knees) == 0:
        knee = None
    else:
        # The best knee is the one where the curve difference is the highest
        # (where the most sudden change in sharpness is found)
        knee = max(knees, key=itemgetter(1))[0]
    return knee


def compute_effective_mp(img):
    w, h = img.size

    # Ensure that there is plenty of room to downscale
    if w <= MIN_RESOLUTION_WIDTH * 1.2:
        print("ERROR: image width (%s) is too close to the MIN_RESOLUTION_WIDTH (1.2x == %s)" % (str(w), str(MIN_RESOLUTION_WIDTH*1.2)))
        return None

    # Compute downscaling resolutions
    if DOWNSCALE_EXPONENTIALLY:
        widths = (1 - (np.linspace(0.0, 1.0, num=NUM_DOWNSCALES)**2)) * (w-MIN_RESOLUTION_WIDTH) + MIN_RESOLUTION_WIDTH
    else:
        widths = np.flip(np.linspace(MIN_RESOLUTION_WIDTH, w, NUM_DOWNSCALES))
    h_ratio = h/w
    heights = np.floor(h_ratio * widths).astype('int')
    widths = np.floor(widths).astype('int')
    sizes = list(zip(widths, heights))
    
    # Compute the pixel-level contrast per downscaled image
    contrast = []
    for i in tqdm(range(NUM_DOWNSCALES)):
        new_size = sizes[i]
        downscaled_img = img.resize(new_size)
        c = compute_contrast(downscaled_img)
        contrast.append(c)

    megapixels = [s[0]*s[1]/1000000 for s in sizes]
    x = megapixels
    y = contrast
    
    # Find possible knees
    knee = find_knee(x, y)

    # Optionally plot the sharpness vs. downscaled images
    if SHOW_PLOT:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        plt.plot(x, y, label='Contrast per image size')
        plt.scatter(x, y, label='Contrast per image size')
        if knee is not None:
            plt.vlines(knee, plt.ylim()[0], plt.ylim()[1], linestyles='dashed')
        plt.xlabel('Megapixels')
        plt.ylabel('Sharpness')
        if x[0] > 3:
            plt.xticks(range(0, x[0].astype(int)+1, 1))
        plt.grid(True)
        if knee is not None:
            fig.canvas.set_window_title('Effective Resolution: %.1f E-MP' % knee)
            plt.title('Effective Resolution: knee = %.1f E-MP' % knee)
        else:
            plt.title('Sharpness per downscaled image (no knee was found)')
            fig.canvas.set_window_title('Effective Resolution: unknown')
        plt.show()

    return knee
