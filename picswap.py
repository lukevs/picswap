"""PICSWAP - Rearranges one image to look like another."""

import sys
from os import path

import numpy as np
from scipy import misc
from skimage import color


def argsort_by_value(arr):
    """Argsorts the array by HSV value

    :param arr: image array to argsort
    :type arr: numpy.ndarray

    :returns: linearized indices to sort arr
    :rtype: numpy.ndarray
    """

    as_hsv = color.rgb2hsv(arr.reshape(1, -1, 3))
    values = as_hsv[:,:,2]
    return np.argsort(values.reshape(-1))


def swap(first, second, argsort=None):
    """Rearranges the pixels in one image to create resemble another

    :param first: image to rearrange
    :type first: numpy.ndarray

    :param second: image to rearrange into
    :type second: numpy.ndarray

    :param argsort: function to argsort an image
    :type argsort: function

    :returns: the rearranged image
    :rtype: numpy.ndarray
    """

    # set argsort
    if argsort is None:
        argsort = argsort_by_value

    # scale first if necessary
    first = concatenate_to_scale(first, second.size)

    # sort first
    first = first.reshape(-1, 3)[argsort(first)]

    # reverse argsort second
    rearranged = argsort(second).argsort()

    return first[rearranged].reshape(second.shape)


def concatenate_to_scale(arr, size):
    """Concatenates an array onto itself until it is at least size

    :param arr: arr to scale
    :type arr: numpy.ndarray

    :param size: size to scale to or above
    :type size: int

    :returns: the scaled array
    :rtype: numpy.ndarray
    """

    while arr.size < size:
        arr = np.concatenate((arr, arr))

    return arr


def main(argv):

    firstpath = argv[0]
    secondpath = argv[1]

    dir = path.dirname(secondpath)

    firstbase = path.basename(firstpath)
    secondbase = path.basename(secondpath)
    savepath = path.join(dir, firstbase[:-4] + "_to_" + secondbase)

    print("opening")
    first = misc.imread(firstpath)
    second = misc.imread(secondpath)

    print("swapping")
    img = swap(first, second)

    print ("saving")
    misc.imsave(savepath, img)


if __name__ == "__main__":
    main(sys.argv[1:])
