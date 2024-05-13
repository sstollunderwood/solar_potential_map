Noboru☀

Noboru is a deep learning model built with PyTorch and hosted with Streamlit with the aim of identifying rooftop space viable for solar generation. This app can help local governments calculate their total rooftop space as well as how much solar energy could be generated and how much CO2 could be offset if this space was utilized.  

Using a prelabeled dataset of aerial photographs of Japan provided by the [Geospatial Information Authority of Japan](https://gisstar.gsi.go.jp/gsi-dataset/09/index.html), we retrained [Meta's Segment Anything Model (SAM)](https://segment-anything.com/) to build a model that identifies rooftops.

The GSI dataset only labeled wooden buildings and buildings under three stories tall, which majorly limits the classifying capabilities of the final model. 


Getting Started
Setup
Install requirements

pip install -r requirements.txt
ENV Variables
Create .env file

touch .env
Inside .env, set these variables. For any APIs, see group Slack channel.

MAPS_API_KEY==your_own_key
API_RUN=LOCAL
MODEL_TARGET=local
Built With
SAM - Base Model
PyTorch - Model Re-Training
FastAPI - Back-end API to process input images
Docker - Container to host our API on the web
Streamlit - Frontend
OpenCV — For image processing and handling

Acknowledgements
This project could not have been completed without tremendous help from my team mates and the Le Wagon TAs.

Team Members
Ryan Tenbarge
Mark Jarrett
Sam Wolf
