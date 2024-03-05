FROM python:3.10.6-buster

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
# RUN apt-get update && apt-get install libgl1
# Run this once. libpencvdev needs the two updates.

# COPY THE REST OF THE FILES ONLY AFTER THE PIP INSTALL ; AND TRY NOT TO CHANGE IT

COPY retrain_weights /retrain_weights
COPY utils /utils
COPY fast.py /fast.py
COPY test_api.py /test_api.py

# put this later so it doesn't rerun every time

CMD uvicorn fast:app --host 0.0.0.0 --port $PORT
