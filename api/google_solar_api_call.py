import requests

def building_insights(latitude, longitude, APIkey): # returns insights
    url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={latitude}&location.longitude={longitude}&requiredQuality=HIGH&key={APIkey}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return ''
