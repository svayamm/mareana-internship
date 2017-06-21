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
from collections import defaultdict
import pandas as pd
from pathlib2 import Path
from . import find_matches_script

class FindMatchingImages(object):
    """docstring for FindMatchingImages.
    """
    def __init__(self):
        self.threshold = 100 # arbitrary value
        self.labels_images_path = Path('img_sim/classifier-labels/images')
        # assuming directory structure of Unclassified has
        # folders for individual images; while Labels are
        # 'flattened' - i.e. no subdirectories
        self.unclassified_path = Path('img_sim/unclassified-imgs-copy')

        self.label_images_list = self.create_image_list(self.labels_images_path)

        self.unclassified_list = [str(x.name) for x in self.unclassified_path.iterdir() if x.is_dir()]

        self.result_dict = defaultdict(dict)

    def run(self):
        """ docstring for main run function """
        for lbl_img in self.label_images_list:
            self.result_dict[lbl_img] = defaultdict(list)

        self.fill_results_dict()
        self.verify()
        # print(sorted(self.result_dict.keys()))
        self.format_csv()

    def fill_results_dict(self):
        """ docstring for fill_results_dict function
        regarding efficiency -
        nested for loop results in higher-order polynomial
        complexity; necessitated due to pairwise comparison?

        Path.iterdir() v os.scandir()
        """
        for lbl_img in self.label_images_list:
            for x in self.unclassified_path.iterdir():
                if x.is_dir():
                # x is a main file directory -
                # e.g. directory for img 'abc001'

                    sub_level_imgs = self.create_image_list(x)
                    # list of 'dissected' levels of main
                    # file - 'abc001_L2_15, abc001_L7_0' etc

                    x_dist = self.classify_sub_images(lbl_img, sub_level_imgs, x)

                    self.result_dict[lbl_img][str(x.name)] = filter(lambda d: d < self.threshold, x_dist)
                    # print(len(filter(lambda d: d < self.threshold, x_dist)))

    
    def create_image_list(self, image_path):
        """ docstring for main run function """
        if not image_path.exists():
            print('Image path does not exist!')
            return
        elif not image_path.is_dir():
            print('Image path is not a directory!')
            return
        else:
            # obtains list of .png files in given directory
            # -- can adjust to find multiple filetypes
            images = image_path.glob('*.png')
            image_list = [str(image.name) for image in images if not str(image.name).startswith('._')]
            return image_list

    def classify_sub_images(self, lbl_img, sub_lvl, x_path):
        """ x_path : the path to the 'containing' image
        (e.g. abc001) from which the sub-levels have been
        dissected (e.g. abc001_L0_1, abc001_L1_0)
         """
        lbl_img_path = self.labels_images_path / lbl_img
        dist_x = []
        # list of distances of each sub_level_image
        # (e.g. abc001_L0_12 or abc002_L17_35, etc.) to the
        # given label

        for img_x in sub_lvl:
            img_x_path = x_path / img_x
            if not lbl_img_path.exists():
                print('Label image path does not exist!')
            if not img_x_path.exists():
                print('Image path B does not exist!')
            else:
                dist_to_label = find_matches_script.find_distance(str(img_x_path), str(lbl_img_path))
                dist_x.append(dist_to_label)
        # print(len(dist_x))
        return dist_x

    def format_csv(self):
        """ docstring for format_csv function """
        data_frame = pd.DataFrame({label : list(map(lambda x: len(x), results.values())) for label, results in self.result_dict.items()},index=self.unclassified_list)
        data_frame.to_csv('img_results.csv')
        

    def verify(self):
        # print(sorted(self.result_dict.keys()) == sorted(self.label_images_list))
        # print('AB')
        for label, matches in self.result_dict.items():
            
            # print(label, sorted(matches.keys()) == sorted(self.unclassified_list))
            # print(label, sorted(matches.keys()))
            print (map(lambda x: len(x), matches.values()))
            print()

if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
