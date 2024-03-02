import cv2
from PIL import Image
import numpy as np
import requests

# load the image
test_image = Image.open("data_for_ml/google_images/4.png")

# convert image to numpy array
image_np = np.array(test_image)
print(image_np.shape)

# prepare the data as JSON
data = {'image': image_np.tolist()}
if type(data['image']) == list:
    print('Numpy array successfully converted to Nd list')

# send a POST request to the API endpoint
api_url = "http://127.0.0.1:8000/predict"
response = requests.post(api_url, json=data)

# check if the request was successful
if response.status_code == 200:
    # get the response data
    response_data = response.json()
    output_image_np = np.array(response_data['output_mask'])

    # try saving the output mask to a local file
    # we need to tell it that the np array is grayscale, otherwise it will just be a black image
    result = cv2.normalize(output_image_np, dst=None, alpha=0,
                           beta=255,norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    cv2.imwrite('output_mask_test_4.png', result)
    print(f'Shape of output image array: {output_image_np.shape}')
else:
    print('Error', response.status_code)
    print(response.text)
