import os
import sys
# Download and install the pathlib2 library using Miniconda3
from pathlib2 import Path
from . import find_matches_script

class FindMatchingImages(object):
    """docstring for FindMatchingImages.
    Using python 2.7.* on Miniconda3
    Run with python -m img_sim
    """

    def run(self):
        self.imgFilePath = Path('img_sim/test_output_img')
        self.outputFile = open('img_sim/results.txt', 'w+')

        if not self.imgFilePath.exists():
            print 'Image path does not exist!'
        elif not self.imgFilePath.is_dir():
            print 'Image path is not a directory!'
        else:
            # obtains list of .png files in given directory
            # -- can adjust to find multiple filetypes

            images = self.imgFilePath.glob('**/*.png')
            image_list = [image for image in images]
            # creates a 'handshake dictionary' -- explained in function
            hs_dict = create_handshake_dict(image_list)
            # print(len(hs_dict.keys()))
            # lens = [len(hs_dict[key]) for key in hs_dict.keys()]
            # print(lens)
            # print(sorted(lens))
            find_matches_script.main(hs_dict, self.outputFile)


def create_handshake_dict(imageList):
    """docstring for create_handshake_dict.

    Based on http://mathworld.wolfram.com/HandshakeProblem.html.

    """
    handshake = {}
    default = None
    for file1 in imageList[:-1]:
      if str(file1) not in handshake.keys():
        handshake[str(file1)] = set()
      for file2 in imageList:
        if file1 == file2:
          continue
        elif (handshake.get(str(file2), default) is None):
          handshake[str(file1)].add(str(file2))
    return handshake

if __name__ == '__main__':
    obj = FindMatchingImages()
    obj.run()
