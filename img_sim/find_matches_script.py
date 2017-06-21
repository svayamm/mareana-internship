import os
import sys
import numpy as np
import cv2

def find_distance(image_1, image_2):
    """ docstring for find_distance
    
    - makes assumption that images being passed in are of
    same size; else resize to same size
    - 

    Using a FLANN-based feature matcher with the ORB algorithm to find matching
features between 2 given images. The Hamming distance between the feature
descriptors is calculated; with a lower distance indicating a better match in
features.

The average of the 10 best (lowest distance) matches is used as an indicator of
the similarity of the given images.
    """
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
    # get average distance of all matches 
    averageDist = sum(distances)/float(len(distances))

    return averageDist

def main(handshake_dict, output_file):
    """ docstring for main function 
    
    """
    # assuming length of arguments passed in should be 2
     
    

    for image_a in handshake_dict:
        same_list = filter(lambda x: find_distance(image_a, x) < same_threshold, handshake_dict[image_a])
        # same_list will return a list of images 
        # with an avg. distance less than the 'same' 
        # threshold
        output_file.write('File: %s, Same images: %s \n' % (image_a, str(same_list)))

if __name__ == '__main__':
    # assuming argv[1] and argv[2] are the handshake dict
    # and the output file location, passed in when the
    # find_matches_script is called from the __main__ file.
    main(sys.argv[1], sys.argv[2])
