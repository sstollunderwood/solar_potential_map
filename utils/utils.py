import requests
from PIL import Image
import numpy as np

def watermark_remover(url):
    #Takes the Google Maps API Image and returns it without the watermark
    im = Image.open(requests.get(url,stream=True).raw)
    return im.crop((0,0,572,572))

def pixel_size_calculator(zoom,lat):
    #Given a zoom level and lattitude, returns area of a pixel
    #Based on the assumption earth's radius = 6378137m

    #Get pixel length
    pixel_length = 156543.03392 * np.cos(lat * np.pi / 180) * (2 ** zoom)

    #Return pixel area
    return pixel_length ** 2
