"""
This script accompanies the __main__ file for the img_sim
module.

Uses the following libraries, installed through Miniconda3:
    - numpy
    - imutils
    - OpenCV 2.x (as cv2)

This script has been written to run on Python 2.7.x -- it 
will NOT work with OpenCV 3 / Python 3, due to issues with 
the Python binding for OpenCV3.
"""
import numpy as np
import imutils
import cv2

def find_distance(image_1_path, image_2_path, algo):
    """ docstring for find_distance
    
    - makes assumption that images being passed in are of
    same size; else resize to same size
    - 
@image_1_path : Unclassified
@image_2_path : Label (i.e. template)

algo = "T_M" -- template matching; "F_M" -- feature matching
    """
    # Converting to grayscale; assuming images are already of same size
    image1 = cv2.imread(image_1_path)
    img1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2 = cv2.imread(image_2_path)
    img2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    if algo == "F_M":
        """
        Using a FLANN-based feature matcher with the ORB algorithm to find 
        matching features between 2 given images. The Hamming distance between 
        the feature descriptors is calculated; with a lower distance indicating 
        a better match in features.
        The average of the matches is used as an indicator of the similarity of 
        the given images.
        
        """
        # Initiate ORB detector
        orb = cv2.ORB()

        # find the keypoints and descriptors with ORB
        # TODO: Memoize to reduce # of expensive calls
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        # create BFMatcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # Match descriptors.
        matches = bf.match(des1,des2)
        

        # # Sort them in the order of their distance.
        # matches = sorted(matches, key = lambda x:x.distance)    

        # distances = [0 for i in xrange(len(matches))]
        # for i,(a, b) in enumerate(matches):
        #     distances[i] = a.distance
        # # get average distance of all matches 
        # averageDist = sum(distances)/float(len(distances))
        if len(matches) > 0:
            distances = map(lambda x:x.distance, matches)
            # get average distance of all matches 
            averageDist = np.average(distances)
            # print(len(matches), averageDist)
            return averageDist
        else: 
            # avoid NaN error with arbiratily high dist
            return 999

    elif algo == "T_M":

        # Detect edges in label image using Canny edge detector

        template = cv2.Canny(img2, 50, 200)
        (tH, tW) = template.shape[:2]

        # loop over the scales of the image in order to
        # 'make' the template matcher scale-invariant
        # Based on http://www.pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv/

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # resize the image according to the scale
            resized = imutils.resize(img1, width=int(img1.shape[1]*scale))

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
            # matrix / map of comparisons at each point
            # If image is W * H and templ is w * h , then result is (W-w+1) * (H-h+1)

            threshold = 0.95
            locations = np.where((result>=threshold).all())
     
            # locations where matches are found
            # i.e. correlation coefficient >= threshold

            matching_points = zip(*locations[::-1])
            return matching_points
