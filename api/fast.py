# from google_solar_api_call import building_insights # comment this out because docker will look for it in the root folder, when it's actually in /api
# from sam_model import prediction_function
from dotenv import load_dotenv # Fetch APIkey
from fastapi import FastAPI
import os # To use .env in fast.py

app = FastAPI()
load_dotenv()

APIkey = os.environ.get("APIkey")

@app.get("/prediction")
def get_sam_model_prediction(image): # Send this image to the model
    # Call prediction function here
    return {"mask":1}, {"rooftop_area":"num_pixels"}

@app.get('/')
def root():
    return {'api':'online'}
