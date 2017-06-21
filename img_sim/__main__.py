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
import pandas as pd
from pathlib2 import Path
from collections import defaultdict
from . import find_matches_script

class FindMatchingImages(object):
    """docstring for FindMatchingImages.
    
    """

    def run(self):
        """ docstring for main run function """
        # same_threshold = 20 # arbitrary value
        self.labels_images_Path = Path('img_sim/classifier-labels/images')
        # assuming directory structure of Unclassified has
        # folders for individual images; while Labels are
        # 'flattened' - i.e. no subdirectories 
        self.unclassified_Path = Path('img_sim/unclassified-imgs-copy')
        self.output_Path = Path('img_sim/test_output_img')

        # self.labels_list = [str(x) for x in self.labels_Path.iterdir() if x.is_dir()]

        label_images_list = create_image_list(self.labels_images_Path)
        # unclassified_images = create_image_list()

        self.result_dict = defaultdict(dict)

        for lbl_img in label_images_list:
            # lbl_img_path = resolve
            result_dict[lbl_img] = defaultdict(list) 


        find_matches_script.main(hs_dict, output_File)

    # def create_new_empty_folders(self):
    #     """ docstring for main run function """
    #     for label in self.labels_list:
    #         # new_dir = Path resolve (output_path+label)
    #         # if not new_dir.exists():
    #         #     os.makedirs()
    #         continue

    
    def create_new_empty_folders(self):
        """ docstring for main run function 
        
        regarding efficiency - 
        nested for loop results in higher-order polynomial
        complexity

        Path.iterdir() v os.scandir()
        
        """
        for lbl_img in label_images_list:
            # lbl_img_path = resolve
            for x in self.unclassified_Path.iterdir():
                if x.is_dir(): 
                # x is a main file directory -
                # e.g. directory for img 'abc001'
                    sub_level_imgs = create_image_list(x)
                    # list of 'dissected' levels of main
                    # file - 'abc001_L2_15, abc001_L7_0' etc

            continue

    def create_image_list(self, img_Path):
        """ docstring for main run function """
        if not img_Path.exists():
            print('Image path does not exist!')
            return
        elif not img_Path.is_dir():
            print('Image path is not a directory!')
            return
        else:
            # obtains list of .png files in given directory
            # -- can adjust to find multiple filetypes
            images = img_Path.glob('**/*.png')
            image_list = [image for image in images]
            return image_list

    def classify_images(self, self.unclassified_list):
        """ docstring for main run function """
        # return_dict = {label:[] for label in self.labels_list}
        for label in self.labels_list:
            # label_path = self.classified_labels_path + label
            # if not (self.label_path.exists() and label_path.is_dir() and os.listdir(label_path)):
                # print 'self.invalid label_path' 
            continue
        return return_dict
    
def format_csv():
    """ docstring for main run function """
    # stuff
    return

if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
