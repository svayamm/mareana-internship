"""
Uses OpenCV 2.x and Python 2.7.x, installed through Miniconda3
-- this will NOT work with OpenCV 3 / Python 3, due to issues with the Python
binding.

Using a FLANN-based feature matcher with the ORB algorithm to find matching
features between 2 given images. The Hamming distance between the feature
descriptors is calculated; with a lower distance indicating a better match in
features.

The average of the 10 best (lowest distance) matches is used as an indicator of
the similarity of the given images.
"""

import numpy as np
import cv2
# from skimage import measure


# Constant definitions
SIM_IMAGE_SIZE = (640, 480)

# Converting to grayscale and resizing to same size
img1 = cv2.resize(cv2.imread('test_img/MonaLisa_1.jpeg', cv2.IMREAD_GRAYSCALE), SIM_IMAGE_SIZE)
img2 = cv2.resize(cv2.imread('test_img/coastline.jpg', cv2.IMREAD_GRAYSCALE), SIM_IMAGE_SIZE)

# Initiate ORB detector
orb = cv2.ORB()

# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

matches = flann.knnMatch(np.float32(des1), np.float32(des2), k=2)
# must convert descriptors to 32-bit float



distances = [0 for i in xrange(len(matches))]
for i,(a,b) in enumerate(matches):
    distances[i]=a.distance
# Sort them in the ascending order of their distance.
distances = sorted(distances)


# get average distance of top 10 matches (lowest 10 distances)
averageDist = sum(distances[:10])/10.0

print "Average feature distance (lower is better):", averageDist
