FROM python:3.10.6-buster

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Run this once

# COPY THE REST OF THE FILES ONLY AFTER THE PIP INSTALL ; AND TRY NOT TO CHANGE IT

COPY api /api
# put this later so it doesn't rerun every time

CMD uvicorn api.fast:app --host 0.0.0.0 --port 8080
