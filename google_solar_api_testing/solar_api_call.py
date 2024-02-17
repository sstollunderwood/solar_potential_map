import requests

def data_layers(latitude, longitude, radius): # returns image and mask layer
    url1 = f"https://solar.googleapis.com/v1/dataLayers:get?location.latitude={latitude}&location.longitude={longitude}&radiusMeters={radius}&view=FULL_LAYERS&requiredQuality=HIGH&pixelSizeMeters=0.5&key=AIzaSyBMq9USaxYUKJyC4YUC66xiu2si28UiiSI"
    try:
        response = requests.get(url1)
        return response.json()
    except:
        return ''

def building_insights(latitude, longitude): # returns insights
    url2 = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={latitude}&location.longitude={longitude}&requiredQuality=HIGH&key=AIzaSyBMq9USaxYUKJyC4YUC66xiu2si28UiiSI"
    try:
        response = requests.get(url2)
        return response.json()
    except:
        return ''
