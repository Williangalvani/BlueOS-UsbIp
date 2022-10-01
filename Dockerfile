from python:3.9-slim-bullseye

RUN apt update && apt install -y sshpass

COPY app /app
RUN python /app/setup.py install

COPY app/static/index.html /app/static/index.html
COPY app/main.py /app/main.py

LABEL version="1.0"
LABEL permissions '\
{\
    "NetworkMode": "host"\
}'
LABEL reasonings = '{\
    "network_mode": "Default option"\
}'

LABEL requirements="core >= 1"

ENTRYPOINT cd /app && python main.py
