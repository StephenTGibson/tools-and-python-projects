# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 19:43:29 2021

@author: sgibs

call from command line:
python resize_images.py -p "testing/*.jpg"

ensure a destination folder of the same name is already 
created within source image folder

"""

#from __future__ import annotations
#import os
import glob
from pathlib import Path
#import sys
import click
from PIL import Image

#SUPPORTED_FILE_TYPES = ['.jpg', '.png']

def process_image(image_fp, width_new):
    
    #open
    im = Image.open(image_fp)
    #resize
    height_new = int(im.size[1]*(width_new/im.size[0]))
    im = im.resize((width_new,height_new))
    #rename
    image_fp_str = str(image_fp)
    folder = image_fp_str[: image_fp_str.rindex('\\')] + '/'
    album_name = image_fp_str[: image_fp_str.rindex('\\')] + '-'
    image_name = image_fp_str[image_fp_str.rindex('\\') +1 : image_fp_str.rindex('.')] + '-'
    image_size = str(width_new) + 'x' + str(height_new)
    #save
    im.save(folder + folder +\
            album_name + image_name + image_size +\
            '.jpg',
              'jpeg')

#pattern = "testing/*.jpg"

@click.command()
@click.option("-p", "--pattern", help='folder & file type ("folder/*.jpg")')
@click.option("-w", "--width", default=800, help='width of resized image in px')
def main(pattern, width):
    count = 0
    for image_fp in images:=(Path().glob(pattern)):    
        process_image(image_fp, width)        
        count += 1
    print(str(count) + ' images processed')
    

if __name__ == '__main__':
    main()