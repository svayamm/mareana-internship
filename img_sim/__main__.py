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
        img_File_Path = Path('img_sim/test_output_img')
        output_File = open('img_sim/results.txt', 'w+')

        create_image_list()

            # creates a 'handshake dictionary' -- explained in function
            hs_dict = create_handshake_dict(image_list)

            find_matches_script.main(hs_dict, output_File)
            output_File.close()


# def create_handshake_dict(imageList):
#     """docstring for create_handshake_dict.

#     Based on http://mathworld.wolfram.com/HandshakeProblem.html.

#     """
#     handshake = {}
#     default = None
#     for file1 in imageList[:-1]:
#         if str(file1) not in handshake.keys():
#             handshake[str(file1)] = set()
#         for file2 in imageList:
#             if file1 == file2:
#                 continue
#             elif handshake.get(str(file2), default) is None:
#                 handshake[str(file1)].add(str(file2))
#     return handshake

def create_new_empty_folders():
    # stuff

def create_image_list():

    if not img_File_Path.exists():
        print('Image path does not exist!')
    elif not img_File_Path.is_dir():
        print('Image path is not a directory!')
    else:
        # obtains list of .png files in given directory
        # -- can adjust to find multiple filetypes
        images = img_File_Path.glob('**/*.png')
        image_list = [image for image in images]

def classify_images():
    # stuff

def sort_folders():
    # stuff

if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
