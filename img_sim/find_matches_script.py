import os
import sys
import numpy as np
import cv2

# Constant definitions
SIM_IMAGE_SIZE = (640, 480)

def find_distance(image_1, image_2):
    # Converting to grayscale; assuming images are already of same size
    img1 = cv2.imread(image_1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_2, cv2.IMREAD_GRAYSCALE)

    # Initiate ORB detector
    orb = cv2.ORB()

    # find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # FLANN parameters -- default values; taken from OpenCV documentation
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(np.float32(des1), np.float32(des2), k=2)
    # must convert descriptors to 32-bit float

    distances = [0 for i in xrange(len(matches))]
    for i,(a, b) in enumerate(matches):
        distances[i] = a.distance
    # Sort them in the ascending order of their distance.
    distances = sorted(distances)
    # get average distance of top 10 matches (lowest 10 distances)
    averageDist = sum(distances)/float(len(distances))
    # averageDist = sum(distances[:10])/10.0

    return averageDist

def main(handshake_dict, output_file):
    """ docstring for main function """
    # assuming length of arguments passed in should be 2

    # output_file.truncate() # wipe file of previous results
    for image_a in handshake_dict:
        for image_b in handshake_dict[image_a]:
            dist = find_distance(image_a, image_b)
            print('File 1: %s, File 2: %s, Distance: %f' % (image_a, image_b, dist))

if __name__ == '__main__':
    main(sys.argv[1:])
