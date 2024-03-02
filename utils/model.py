from transformers import SamModel, SamConfig, SamProcessor
import torch
import numpy as np
from google.cloud import storage
from PIL import Image
import gdown

def load_model_locally(path):
    """Loads retrained SAM model weights from local file
    and returns model ready to make a prediction"""
    # Load the model configuration
    model_config = SamConfig.from_pretrained("facebook/sam-vit-base")
    # Create an instance of the model architecture with the loaded configuration
    model = SamModel(config=model_config)
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    return model

def load_model_from_cloud(bucket_name: str, blob_name: str):
    """Downloads retrained SAM model weights from google cloud bucket and
    returns model ready to make a prediction"""
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    #data = blob.download_to_file()
    # Load the model configuration
    model_config = SamConfig.from_pretrained("facebook/sam-vit-base")
    # Create an instance of the model architecture with the loaded configuration
    model = SamModel(config=model_config)
    model.load_state_dict(torch.load(blob))
    return model


def predict_mask(model, image) -> np.array:
    """Takes in a retrained SAM and a google earth
    satellite image in .png format of any size and outputs a black and white image
    corresponding to rooftop masks. Output size is xxx by xxx."""
    processor = SamProcessor.from_pretrained("facebook/sam-vit-base")
    if type(image) != np.array:
        image_array = np.array(image)
    else:
        image_array = image
    array_size = image_array.shape[0]
    # Higher grid sizes seem to confuse the model and decrease performance
    grid_size = 10
    # Generate grid points which will serve as prompt for SAM
    x = np.linspace(0, array_size-1, grid_size)
    y = np.linspace(0, array_size-1, grid_size)
    # Generate a grid of coordinates
    xv, yv = np.meshgrid(x, y)
    # Convert the numpy arrays to lists
    xv_list = xv.tolist()
    yv_list = yv.tolist()
    # Combine the x and y coordinates into a list of list of lists
    input_points = [[[int(x), int(y)] for x, y in zip(x_row, y_row)] for x_row, y_row in zip(xv_list, yv_list)]
    #We need to reshape our nxn grid to the expected shape of the input_points tensor
    # (batch_size, point_batch_size, num_points_per_image, 2),
    # where the last dimension of 2 represents the x and y coordinates of each point.
    #batch_size: The number of images you're processing at once.
    #point_batch_size: The number of point sets you have for each image.
    #num_points_per_image: The number of points in each set.
    input_points = torch.tensor(input_points).view(1, 1, grid_size*grid_size, 2)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    inputs = processor(image_array, input_points=input_points, return_tensors="pt")
    # Move the input tensor to the GPU if it's not already there
    inputs = {k: v.to(device) for k, v in inputs.items()}
    model.eval()
    # forward pass
    with torch.no_grad():
        outputs = model(**inputs, multimask_output=False)
    # apply sigmoid
    mask_prob = torch.sigmoid(outputs.pred_masks.squeeze(1))
    # convert soft mask to hard mask
    mask_prob = mask_prob.cpu().numpy().squeeze()
    mask_prediction = (mask_prob > 0.5).astype(np.uint8)
    return mask_prediction


# Use Mark's to account for curvature of the earth
# def get_roof_area(mask: np.array, zoom_level=19):
#     """Accepts a mask created in by the predict_mask function to calculates
#     the ground area of white pixels (rooftops) in the input image.
#     Assuming a ground-zoom level=19, the relative area of each pixel is
#     2.5 square meters"""
#     # zoom_level_GSD dictionary can allow for different levels of zoom.
#     # Each key is the zoom level, and each value is the corresponding
#     # area of each pixel in square meters. We can add more zoom
#     # levels later if we want.
#     zoom_level_GSD = {19: .25**2}
#     white_pixel_count = np.count_nonzero(mask)
#     rooftop_area = white_pixel_count * zoom_level_GSD[zoom_level]
#     return rooftop_area
