from python:3.9-slim-bullseye

RUN apt update && apt install -y sshpass

COPY app /app
RUN python /app/setup.py install

COPY app/static/index.html /app/static/index.html
COPY app/main.py /app/main.py

LABEL version="1.0.1"
LABEL permissions='\
{\
    "NetworkMode": "host"\
}'
LABEL authors='[\
    {\
        "name": "Willian Galvani",\
        "email": "willian@bluerobotics.com"\
    }\
]'
LABEL company='{\
        "about": "",\
        "name": "Blue Robotics",\
        "email": "support@bluerobotics.com"\
    }'
LABEL type="device-integration"
LABEL tags='[\
        "communication"\
    ]'
LABEL readme='https://raw.githubusercontent.com/Williangalvani/BlueOS-UsbIp/{tag}/Readme.md'
LABEL links='{\
        "website": "https://github.com/Williangalvani/BlueOS-UsbIp",\
        "support": "https://github.com/Williangalvani/BlueOS-UsbIp"\
    }'
LABEL requirements="core >= 1.1"

ENTRYPOINT cd /app && python main.py
