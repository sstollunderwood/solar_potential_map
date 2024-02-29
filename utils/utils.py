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

def solar_panel_energy_output(area, location="tokyo", setback=0.75, efficiency=0.20):
    #Returns annual solar panel output energy taking panel efficiency, setback, and average annual solar radiation into account
    #Annual Solar Radiation based on 5 year average values from https://www.data.jma.go.jp/obd/stats/etrn/view/monthly_s3_en.php?block_no=47662&view=11
    location = location.lower().strip()
    radiation_dict = {"tokyo":13.64,"osaka":14.72,"nagoya":14.64,"fukuoka":14.1,"sapporo":13.04}
    sunshine_dict = {"tokyo":2035.28,"osaka":2214.84,"nagoya":2227.46,"fukuoka":2051.74,"sapporo":1907.68}
    sunshine_hours = sunshine_dict[location]

    #Convert radiation from MJ/m2 to KWh/m2
    radiation = (radiation_dict[location] * 1000000) / 3600000

    return ((area * setback) * radiation * sunshine_hours) * efficiency

def co2_calculator(solar_panel_output, solar_carbon_intensity=0.041, carbon_intensity=0.376):
    #Returns estimate of how much kg of carbon is offset by a given power amount produced by solar panels

    return solar_panel_output * (carbon_intensity - solar_carbon_intensity)
