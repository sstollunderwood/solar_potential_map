import requests
from PIL import Image
import numpy as np
from utils.params import *

def get_gmaps_image(lat,lon,zoom,size="572x594"):
    #Returns Google Maps image with watermark removed
    #Create Google Maps API call
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom={zoom}&size={size}&maptype=satellite&key={MAPS_API_KEY}"

    #Gets the Google Maps API Image and returns it without the watermark
    im = Image.open(requests.get(url,stream=True).raw)
    return im.crop((0,0,572,572))

def rooftop_area_calculator(zoom,lat, mask:np.array):
    #Given a zoom level and lattitude, returns area of a pixel
    #Based on the assumption earth's radius = 6378137m

    #Get pixel length
    pixel_length = 156543.03392 * np.cos(lat * np.pi / 180) / (2 ** zoom)
    pixel_area = pixel_length ** 2
    white_pixel_count = np.count_nonzero(mask)
    #Return pixel area
    return pixel_area * white_pixel_count

def building_insights(latitude, longitude):
    # Retuns Google Solar JSON file
    url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={latitude}&location.longitude={longitude}&requiredQuality=HIGH&key={SOLAR_API_KEY}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return ''
