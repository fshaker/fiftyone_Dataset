import glob
from typing import Tuple
from skimage.measure import label
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from tkinter import filedialog

def get_tissue_mask(image: np.ndarray) -> np.ndarray:

    _ , mask = cv2.threshold(image, 2, 255, cv2.THRESH_BINARY)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  np.ones((5,5), dtype=np.uint8))
    labels = label(mask)
    largestCC = labels == np.argmax(np.bincount(labels.flat)[1:])+1
    return np.asarray(largestCC*255, np.uint8)


def average_histogram(images):
    """
    This function finds the average histogram of a set of images.
    :param images: list of image paths to images' dataset (path like)
    :return: an array of length 256 containing the average histogram
    """
    sum_hist = np.zeros((256, 1), dtype=np.float64)
    num_images = len(images)
    for image in images:
        image_pixels = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        mask = get_tissue_mask(image_pixels)
        hist = cv2.calcHist([image_pixels], [0], mask, [256], [0,256])
        sum_hist += hist
        print(hist.shape)
    return sum_hist/num_images



def calculate_cdf(histogram):
    """
    This method calculates the cumulative distribution function
    :param array histogram: The values of the histogram
    :return: normalized_cdf: The normalized cumulative distribution function
    :rtype: array
    """
    # Get the cumulative sum of the elements
    cdf = histogram.cumsum()

    # Normalize the cdf
    normalized_cdf = cdf / float(cdf.max())

    return normalized_cdf


def calculate_lookup(src_cdf, ref_cdf):
    """
    This method creates the lookup table
    :param array src_cdf: The cdf for the source image
    :param array ref_cdf: The cdf for the reference image
    :return: lookup_table: The lookup table
    :rtype: array
    """
    lookup_table = np.zeros(256)
    for src_pixel_val in range(len(src_cdf)):
        lookup_val = 0
        for ref_pixel_val in range(len(ref_cdf)):
            if ref_cdf[ref_pixel_val] >= src_cdf[src_pixel_val]:
                lookup_val = ref_pixel_val
                break
        lookup_table[src_pixel_val] = lookup_val
    return lookup_table


def match_histograms(src_image, src_mask, ref_hist):
    """
    This method matches the source image histogram to the
    reference histogram
    :param image src_image: The original source image [0-255]
    :param mask source_mask: mask of the source image [0, 255]
    :param image  ref_histe: The reference histogram (length=256)
    :return: image_after_matching
    :rtype: image (array)
    """

    src_hist = cv2.calcHist([src_image], [0], src_mask, [256], [0,256])
    src_cdf = calculate_cdf(src_hist)
    ref_hist_cdf = calculate_cdf(ref_hist)
    lookup_table = calculate_lookup(src_cdf, ref_hist_cdf)
    src_after_matching = cv2.LUT(src_image, lookup_table)
    return src_after_matching*(src_mask>0)

source_images_path = filedialog.askdirectory(title="Select the dataset folder containing the INbreast images")
# source_images_path = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\INbreast Release 1.0\LabelMe_format_equalized"
source_images = glob.glob(os.path.join(source_images_path, '*', '*.png'))
ref_images_path = filedialog.askdirectory(title="Select the private dataset folder ")
# ref_images_path = r"C:\Users\Admin\Documents\VidaMedicals\Codes\Datasets\Segment+Annotate_v2"
ref_images = glob.glob(os.path.join(ref_images_path, '*', '*.png'))
print("Calculating the average histogram ...")
average_hist = average_histogram(ref_images)
print("Finished calculating the average histogram")
for image in source_images:
    print("Processing image {}".format(image))
    image_pixels = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    mask = get_tissue_mask(image_pixels)
    image_after_matching = match_histograms(image_pixels, mask, average_hist)
    cv2.imwrite(image, image_after_matching)


