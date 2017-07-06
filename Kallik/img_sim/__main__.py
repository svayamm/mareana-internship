#!/usr/bin/env python2

"""
Run with '$ python -m img_sim' from containing directory.

This script has been written to run on Python 2.7.x -- it
will NOT work with OpenCV 3 / Python 3, due to issues with
the Python binding for OpenCV3.

Uses the following libraries, installed through Miniconda3:
    - pathlib2
    - pandas
    - numpy
    - imutils
    - OpenCV 2.x (as cv2)

Note: This is just a quick-and-dirty solution.
TODO: Implement proper error-handling methods
TODO: Refactor/distentangle code
TODO: Unit and scalability testing
TODO: Optimise threshold (and other) values, instead of
      using arbitrary values.
"""
############################################################

from collections import defaultdict
from itertools import compress
import shutil
import pandas as pd
from pathlib2 import Path
import find_matches_script


class FindMatchingImages(object):
    """
    The program runs as an instance of the FindMatchingImages class.

    <<Description>>

    Attributes:
            label_images_lst (`list` of `str`): Description of `param3`.
    """

    def __init__(self):
        """
        The various constants and variables are initiated here.

        <<Description>>

        

        """
        ##### Constants #####
        ### These are not expected to change during the
        ### program's execution; though they can be changed
        ### prior to running the program.

        self.labels_images_path = Path('img_sim/classifier-labels/images')
        # assuming directory structure of Labels is
        # 'flattened' - i.e. no subdirectories, all Label 
        # ('benchmark') images in single folder.
        self.unclassified_path = Path('output_png_classified')
        # assuming directory structure of Unclassified has
        # folders for individual images - i.e. sub-level 
        # files (e.g. abc001_L1_14) are grouped into 
        # folders by the file (e.g. abc001) they were 
        # extracted from.
        self.label_images_lst = self.create_image_list(self.labels_images_path)
        # Creates a list of filenames, of all the 'labels'.
        self.algo = "T_M"
        # Set thealgorithm to be used in matcher script
        # T_M = Template Matching
        # F_M = Feature Matching
        self.feat_dist_threshold = 1.63 
        # TODO: change from arbitrary value


        ##### Variables #####

        self.unclassified_list = [str(x.name) for x in self.unclassified_path.iterdir() if x.is_dir()]

        self.result_dict = defaultdict(dict)


    def run(self):
        """ docstring for main run function """
        for lbl_img in self.label_images_lst:
            self.result_dict[lbl_img] = defaultdict(list)

        self.put_unclassified_imgs_in_folders()
        self.fill_results_dict()
        self.format_csv()

    def put_unclassified_imgs_in_folders(self):
        """ docstring for main run function """
        # Sort output_png folder into constituent imgs
        unsorted_imgs = self.create_image_list(self.unclassified_path)
        for img in unsorted_imgs:
            main_name = img.split('_')[0]
            if main_name not in self.unclassified_list:
                new_dir = self.unclassified_path / main_name
                img_path = self.unclassified_path / img
                if not new_dir.exists(): new_dir.mkdir()
                shutil.move(str(img_path), str(new_dir))
        # reinitialise unclassified list to take new folders into account
        self.unclassified_list = [str(x.name) for x in self.unclassified_path.iterdir() if x.is_dir()]

    def fill_results_dict(self):
        """ docstring for fill_results_dict function
        regarding efficiency -
        nested for loop results in higher-order polynomial
        complexity; necessitated due to pairwise comparison?

        Path.iterdir() v os.scandir()
        """
        for lbl_img in self.label_images_lst:
            for x in self.unclassified_path.iterdir():
                if x.is_dir():
                # x is a main file directory -
                # e.g. directory for img 'abc001'

                    sub_level_imgs = self.create_image_list(x)
                    # list of 'dissected' levels of main
                    # file - 'abc001_L2_15, abc001_L7_0' etc

                    if self.algo == "F_M":
                        x_dist = self.classify_sub_images(lbl_img, sub_level_imgs, x)

                        self.result_dict[lbl_img][str(x.name)] = filter(lambda d: d <= self.feat_dist_threshold, x_dist)
                        print(self.result_dict[lbl_img][str(x.name)])

                        bool_dist = map(lambda d: d <= self.feat_dist_threshold, x_dist)
                        matching_sub = list(compress(sub_level_imgs, bool_dist))
                        print(lbl_img, matching_sub)
                    elif self.algo == "T_M":
                        bool_matches = self.classify_sub_images(lbl_img, sub_level_imgs, x)

                        matching_sub = list(compress(sub_level_imgs, bool_matches))
                        # list of sub-lev files that matched

                        self.result_dict[lbl_img][str(x.name)] = matching_sub
    
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
        """ 
        Args:
            x_path: the path to the 'containing' image (e.g. abc001) from which
                the sub-levels have been dissected (e.g. abc001_L0_1,
                abc001_L1_0)
         """
        lbl_img_path = self.labels_images_path / lbl_img
        list_x = []
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
                if self.algo == "F_M":
                    # TODO: keypoints dictionary to reduce
                    # time taken in detect&Compute
                    dist_to_label = find_matches_script.find_distance(str(img_x_path), str(lbl_img_path), self.algo)

                    list_x.append(dist_to_label)
                elif self.algo == "T_M":
                    list_of_points = find_matches_script.find_distance(str(img_x_path), str(lbl_img_path), self.algo)

                    match_found = bool(list_of_points)
                    # false if Null or empty list; else true

                    list_x.append(match_found)
        return list_x

    def format_csv(self):
        """ docstring for format_csv function """
        tup_list = [
        (main, label, sub) 
        for label, results in self.result_dict.iteritems() 
        for main, subs in results.iteritems() 
        for sub in subs
        ]
        data_frame = pd.DataFrame(tup_list, columns=['main_file', 'label_img', 'sub_level_file'])
        data_frame.to_csv('img_results.csv')


if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
