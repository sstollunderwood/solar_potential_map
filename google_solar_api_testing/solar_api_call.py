import requests

def building_insights(latitude, longitude): # returns insights
    url2 = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={latitude}&location.longitude={longitude}&requiredQuality=HIGH&key=AIzaSyBMq9USaxYUKJyC4YUC66xiu2si28UiiSI"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return ''
