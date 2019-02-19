from PIL import Image
import PIL.ImageOps
from pdf2image import convert_from_path
import sys

def invert_all_images(images):

    inverted_images = []

    for image in images:
        inverted_images.append(PIL.ImageOps.invert(image))

    return inverted_images


try:
    # get the path from the command line 
    path = sys.argv[1]
    # convert to image 
    images = convert_from_path(path)   
    inverted = invert_all_images(images) 

    new_path = (path.split('.pdf')[0]) + '_DARK.pdf'
    # save inverted image as pdf
    
    inverted[0].save(new_path, save_all=True, append_images=inverted[1:])
    print('Saved dark PDF!')
except IndexError:
    print('Please provide a path to the file to convert')

