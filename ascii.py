"""
The ascii_magic makes the job easier to return ascii to the terminal.
I however had to tweak the code by subclassing the AsciiArt class in order to rewrite to stdout.
"""


import io
import logging
from os import listdir
from os.path import isfile, join
import os
from pathlib import Path
import sys
from art import text2art

import ascii_magic
import colorama
from PIL import Image, GifImagePlugin
import requests


class AsciiArt(ascii_magic.AsciiArt):
    """
    I looked at the source code on github to figure the method to modify.
    Here is the source code I wanteed to overwrite:
    https://github.com/LeandroBarone/python-ascii_magic/blob/33968afc3622b0ebc243cb5a45bf191ef7df80bd/ascii_magic/_ascii_magic.py#L306
    """


    @staticmethod
    def _print_to_terminal(art: str):
        """
        I overwrite this method from the parent class in order to not "pile" the printed outputs.
        Here I manipulate the stdout to remove what has been printed at every iteration.
        """
        colorama.init()
        print(art)
        num_lines = len(art.split('\n'))
        for _ in range(num_lines):
            sys.stdout.write("\033[F") # special ASCII char to move to previous line
            sys.stdout.write("\033[K") # special ASCII char to delete the following line


class GifAsciiArt(GifImagePlugin.GifImageFile):
    """
    This is a GIF image inherited by Pillow. This delegates the verification and conversion to the library.
    """

    def __init__(self, *args, **kwargs):
        """
        Instantiates the class by calling the mother class' constructor, and feeding with internal methods.
        """
        super().__init__(*args, **kwargs)
        self._pillow_frames=[]
        self._ascii_frames = []
        self.get_pillow_frames()
        self.get_ascii_frames()


    def get_pillow_frames(self):
        """
        Extracts the frames from the animated gif and stores them in a list of created pillow images
        """
        for frame_no in range(self.n_frames):
            self.seek(frame_no)
            new_frame = Image.new('RGB', self.size)
            new_frame.paste(self)
            self._pillow_frames.append(new_frame)
        return self._pillow_frames


    def get_ascii_frames(self):
        """
        Converts pillow image to an ascii representation via a separate class.
        """
        for frame in self._pillow_frames:
            self._ascii_frames.append(AsciiArt(frame))
        return self._ascii_frames


    @property
    def ascii_frames(self):
        return self._ascii_frames


def get_ascii_gif(img_content : io.BufferedIOBase):
    """
    Creates a GifAsciiArt instance if valid content.
    """
    try:
        ascii_gif = GifAsciiArt(img_content)
        return ascii_gif
    except SyntaxError:
        sys.stderr.write(f"Please provide a recognized GIF, provided object: {img_content}\n")
        sys.exit(1)


def print_gif(img, monochrome=False, message=None):
    for ascii_frame in img.ascii_frames:
        ascii_frame.to_terminal(monochrome = monochrome)
    if message:
        print(text2art(message))


def print_ascii_for_files(image_files : list[io.BytesIO], message: str = None, monochrome: bool = False):
    """
    Prints GIF ASCII art for each file in image_files.
    """
    for image_file in image_files:
        ascii_gif = get_ascii_gif(image_file)
        print_gif(ascii_gif, monochrome, message)


def print_ascii_for_folder(directory: Path, message: str = None, monochrome: bool = False, recurse = False):
    """
    Searches for all gif files in a folder and its subfolders (if recursive)
    """
    if recurse:
        filenames = list(directory.rglob("*.[gG][iI][fF]")) # recursive GLOB search on .gif/.GIF files
    else:
        filenames = [directory / f for f in listdir(directory) if isfile(join(directory, f)) and f.lower().endswith(".gif")]
    for filename in filenames:
        with open(filename, 'rb') as file:
            ascii_gif = get_ascii_gif(file)
            print_gif(ascii_gif, monochrome, message)


def print_ascii_for_giphy(giphy_id = None, message: str = None, monochrome: bool = False):
    """
    Requests GIPHY's REST API for a search or
    """
    url_params = {'api_key': os.getenv("GIPHY_API_KEY")}
    if giphy_id is None:
        meta_response = requests.get(f"https://api.giphy.com/v1/gifs/random", params = url_params)
        img_id = meta_response.json()['data']['id']
        logging.debug(meta_response.json()['data']['title'])
    else:
        img_id = giphy_id
    logging.debug(f"image ID provided for GIPHY : {img_id}")
    img_response = requests.get(f"https://i.giphy.com/media/{img_id}/giphy.gif")

    # creating a buffer stream, no need to create a file
    with io.BytesIO() as file:
        file.write(img_response.content)
        file.seek(0)
        ascii_gif = get_ascii_gif(file)
        print_gif(ascii_gif, monochrome, message)
