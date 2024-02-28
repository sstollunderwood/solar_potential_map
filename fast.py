from utils.model import *
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
import numpy as np

app = FastAPI()

# Define a Pydantic model to represent the input data
class InputData(BaseModel):
    image: np.array

    model_config = ConfigDict(arbitrary_types_allowed=True)

# Load the model
app.state.model = load_model_locally('retrain_weights/train_test_split.pth')
if app.state.model:
    print('Model loaded successfully!')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the route to accept POST requests with JSON data containing the Numpy array
@app.post("/predict")
def predict(data: InputData):
    # takes in a json dictionary via the pydantic basemodel object
    # the image key is then used to access the N-d list from the json
    # the list is then converted back to a numpy array and passed in to the prediction function
    try:
        print('Predict endpoint successfully reached!')
        print(f'Type of data being passed in: {type(data.image)}')
        print(f'Shape of input {np.array(data.image).shape}')
        outut_mask = predict_mask(model=app.state.model, image=data.image)
        return {"output_mask": outut_mask.tolist()} # Convert Numpy array to list for JSON serialization
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/')
def root():
    return {'api':'online'}
