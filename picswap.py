# PICSWAP
# Rearranges one image to look like another.

import sys
import numpy as np

from os import path
from scipy import misc
from skimage import color

def argsort_by_value(arr):
    """
    Argsorts the array by HSV value.

    :param arr: image array to argsort
    :type arr: numpy.ndarray
    :returns: linearized indices to sort arr
    """

    as_hsv = color.rgb2hsv(arr.reshape(1, -1, 3))
    values = as_hsv[:,:,2]
    return np.argsort(values.reshape(-1))

def swap(first, second, argsort=argsort_by_value):
    """
    Rearranges the pixels in one image to create resemble another.

    :param first: image to rearrange
    :type first: numpy.ndarray
    :param second: image to rearrange into
    :type second: numpy.ndarry
    :param argsort: function to argsort an image
    :type argsort: function
    :returns: the rearranged image
    """

    # sort first
    first = first.reshape(-1, 3)[argsort(first)]

    # reverse argsort second
    rearranged = argsort(second).argsort()

    return first[rearranged].reshape(second.shape)

def main(argv):

    # manage path
    firstpath = argv[0]
    secondpath = argv[1]

    dir = path.dirname(secondpath)

    firstbase = path.basename(firstpath)
    secondbase = path.basename(secondpath)
    savepath = path.join(dir, firstbase[:-4] + "_to_" + secondbase)

    # open
    print("opening")
    first = misc.imread(firstpath)
    second = misc.imread(secondpath)

    # swap
    print("swapping")
    img = swap(first, second)

    # save
    print ("saving")
    misc.imsave(savepath, img)

if __name__ == "__main__":
    main(sys.argv[1:])
