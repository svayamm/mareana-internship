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
    def __init__(self):
        # same_threshold = 20 # arbitrary value
        self.labels_images_path = Path('img_sim/classifier-labels/images')
        # assuming directory structure of Unclassified has
        # folders for individual images; while Labels are
        # 'flattened' - i.e. no subdirectories
        self.unclassified_path = Path('img_sim/unclassified-imgs-copy')
        # self.output_Path = Path('img_sim/test_output_img')

        self.label_images_list = create_image_list(self.labels_images_Path)
        
        self.unclassified_list = [str(x) for x in self.unclassified_Path.iterdir() if x.is_dir()]
        
        self.result_dict = defaultdict(dict)

        

    def run(self):
        """ docstring for main run function """
        
        for lbl_img in self.label_images_list:
            # lbl_img_path = resolve
            result_dict[lbl_img] = defaultdict(list) 

        find_matches_script.main(hs_dict, output_File)

    
    def fill_results_dict(self):
        """ docstring for main run function 
        
        regarding efficiency - 
        nested for loop results in higher-order polynomial
        complexity; necessitated due to pairwise comparison?

        Path.iterdir() v os.scandir()
        
        """
        for lbl_img in self.label_images_list:
            # lbl_img_path = resolve
            for x in self.unclassified_Path.iterdir():
                if x.is_dir(): 
                # x is a main file directory -
                # e.g. directory for img 'abc001'
                    sub_level_imgs = create_image_list(x)
                    # list of 'dissected' levels of main
                    # file - 'abc001_L2_15, abc001_L7_0' etc

            continue
    
    @staticmethod
    def create_image_list(imgPath):
        """ docstring for main run function """
        if not imgPath.exists():
            print('Image path does not exist!')
            return
        elif not imgPath.is_dir():
            print('Image path is not a directory!')
            return
        else:
            # obtains list of .png files in given directory
            # -- can adjust to find multiple filetypes
            images = imgPath.glob('**/*.png')
            image_list = [image for image in images]
            return image_list

    def classify_images(self, unclassified_list):
        """ docstring for main run function """
        # return_dict = {label:[] for label in self.labels_list}
        for label in self.labels_list:
            # label_path = self.classified_labels_path + label
            # if not (self.label_path.exists() and label_path.is_dir() and os.listdir(label_path)):
                # print 'self.invalid label_path' 
            continue
        return return_dict
    
    def format_csv(self):
        """ docstring for main run function """
        # stuff
        data_frame = pd.DataFrame( { label : pd.Series( \
        [len(matches) for file, matches in results] for \
        label, results in result_dict.items() ) }, index=self.unclass)
        return

if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
