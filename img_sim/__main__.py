############################################################
# img_sim package
# __main__.py
# A python script to find similarity between images
# Author: Svayam Mishra
# Email: svayamm@cmu.edu
# Date: 05 Jun 2017
# Version: 0.3
############################################################
# TODO: notes
"""
Uses OpenCV 2.x and Python 2.7.x, installed through Miniconda3
    -- this will NOT work with OpenCV 3 / Python 3, due to
    issues with the Python binding.

    Run with python -m img_sim from containing directory

    Note: this is just a quick-and-dirty solution - ideally
    proper error-handling methods would be implemented, and
    the code itself would be properly refactored.
    unit testing
    instead of arbitrary values, optimised
    perhaps inbuilt clustering methods used
# Download and install the pathlib2 library using Miniconda3
empty the output folder before running
"""

import os
import sys
from pathlib2 import Path
from . import find_matches_script

class FindMatchingImages(object):
    """docstring for FindMatchingImages.
    
    """

    def run(self):
        """ docstring for main run function """
        self.labels_Path = Path('img_sim/test_output_img')
        self.unclassified_Path = Path('img_sim/test_output_img')
        self.output_Path = Path('img_sim/test_output_img')

        self.labels_list = [str(x) for x in self.labels_Path.iterdir() if x.is_dir()]

        unclassified_images = create_image_list()
        find_matches_script.main(hs_dict, output_File)

def create_new_empty_folders():
    for label in self.labels_list:
        # new_dir = Path resolve (output_path+label)
        # if not new_dir.exists():
        #     os.makedirs()
        continue

def create_image_list(img_Path):

    if not img_Path.exists():
        print('Image path does not exist!')
    elif not img_Path.is_dir():
        print('Image path is not a directory!')
    else:
        # obtains list of .png files in given directory
        # -- can adjust to find multiple filetypes
        images = img_Path.glob('**/*.png')
        image_list = [image for image in images]
    
    return image_list

def classify_images(unclassified_list):
    return_dict = {label:[] for label in self.labels_list}
    for label in self.labels_list:
        # label_path = self.classified_labels_path + label
        # if not (self.label_path.exists() and label_path.is_dir() and os.listdir(label_path)):
            # print 'self.invalid label_path' 
        continue
    return return_dict
    
def sort_folders():
    # stuff

if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
