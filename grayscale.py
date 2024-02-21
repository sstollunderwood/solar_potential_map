import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image


def convert_greyscale(file):
    #Converts pink masked validation photos to black and white

    #Setting up the file paths and image
    current_dir = os.getcwd()
    file = str(file)
    val_data_path = os.path.join(current_dir, 'data_for_ml', 'masked', f'{file}.png')
    destination = os.path.join(current_dir, 'data_for_ml', 'grayscale', f'{file}mask.png')
    my_image = cv2.imread(val_data_path)

    #Create the black and white image
    my_image = np.all(my_image == [255, 0, 255], axis=-1)
    image = Image.fromarray(my_image)

    #Save File
    image.save(destination)


for i in range(1,6001):
    convert_greyscale(i)

for i in range(1,1201):
    convert_greyscale(f'572-{i}')
