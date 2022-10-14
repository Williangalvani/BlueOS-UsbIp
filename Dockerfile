from python:3.9-slim-bullseye

RUN apt update && apt install -y sshpass

COPY app /app
RUN python /app/setup.py install

COPY app/static/index.html /app/static/index.html
COPY app/main.py /app/main.py

LABEL version="1.0.0"
LABEL permissions '\
{\
    "NetworkMode": "host"\
}'
LABEL authors '[\
    {\
        "name": "Willian Galvani",\
        "email": "willian@bluerobotics.com"\
    }\
]'
LABEL docs ''
LABEL company '{\
        "about": "",\
        "name": "Blue Robotics",\
        "email": "support@bluerobotics.com"\
    }'
LABEL readme 'https://raw.githubusercontent.com/Williangalvani/BlueOS-UsbIp/{tag}/Readme.md'
LABEL website 'https://github.com/Williangalvani/BlueOS-UsbIp'
LABEL support 'https://github.com/Williangalvani/BlueOS-UsbIp'
LABEL requirements "core >  1"


ENTRYPOINT cd /app && python main.py
