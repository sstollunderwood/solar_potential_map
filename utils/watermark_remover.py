import numpy as np
from PIL import Image

def watermark_remover(url):
    #Takes the GoogleMaps API Image and returns it without the watermark

    #Get the image
    im = Image.open(requests.get(url,stream=True).raw)

    #Return cropped image
    return im.crop((0,0,572,572))
