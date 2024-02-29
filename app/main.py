#! /usr/bin/env python3
import subprocess
from typing import Any

import uvicorn
from fastapi import FastAPI, status
from fastapi_versioning import VersionedFastAPI, version
from fastapi.staticfiles import StaticFiles
from loguru import logger
import requests

SERVICE_NAME = "UsbIpManager"

user = "pi"
password = "raspberry"

def run_command(command: str, check: bool = True) -> str:
    url = 'http://localhost:9100/v1.0/command/host'
    params = {'command': command, 'i_know_what_i_am_doing': 'true'}
    response = requests.post(url, params=params)
    logger.debug(command)
    logger.debug(response.json())
    # Handle the response as needed
    if response.status_code == 200:
        return response.json()["stdout"]
    else:
        raise Exception("unable to talk to host!")


# logging.basicConfig(handlers=[InterceptHandler()], level=0)
#logger.add(get_new_log_path(SERVICE_NAME))

app = FastAPI(
    title="ZeroTierManager API",
    description="ZeroTierManager is an extension to provice ZeroTier connectivity to BlueOS",
)
# app.router.route_class = GenericErrorHandlingRoute
logger.info("Starting USB IP manager")

@app.get("/command/list", status_code=status.HTTP_200_OK)
@version(1, 0)
async def command_list() -> Any:
    command = f'sudo usbip list -l'
    logger.debug(f"Running command: {command}")
    output = run_command(command)
    logger.debug(output)
    devices = output.split("\n\n")
    organized_devices = []
    for device in devices:
        bus_id = device.split("busid")[1].split(" (")[0].strip()
        device_data = device.split(bus_id)[1].strip()
        organized_devices.append(
            {
                "bus_id": bus_id,
                "device_data" : device_data,
                "exposed": False
            }
        )
    command = f'sudo usbip list --remote localhost'
    logger.debug(f"Running command: {command}")

    # extract ids of devices exposed
    output = run_command(command).strip()
    try:
        data = output.split("localhost")[1].strip().split("\\n")
        for line in data:
          logger.debug(line)
        data = [line.strip() for line in data if line and "           : /" not in line and "           : (" not in line]
        ids = [line.split(": ")[0] for line in data]
         #log all of this
        logger.debug(f"ids: {ids}")
        logger.debug(f"organized_devices: {organized_devices}")
        for device in organized_devices:
            if device["bus_id"] in ids:
                device["exposed"] = True
    except Exception as error:
        print(error)
    return organized_devices



@app.post("/command/bind", status_code=status.HTTP_200_OK)
@version(1, 0)
async def command_bind(device: str) -> Any:
    command = f'sudo usbip bind -b {device}'
    logger.debug(f"Running command: {command}")
    output = run_command(command)
    return output


@app.post("/command/unbind", status_code=status.HTTP_200_OK)
@version(1, 0)
async def command_unbind(device: str) -> Any:
    command = f'sudo usbip unbind -b {device}'
    logger.debug(f"Running command: {command}")
    output = run_command(command)
    return output


app = VersionedFastAPI(app, version="1.0.0", prefix_format="/v{major}.{minor}", enable_latest=True)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Running uvicorn with log disabled so loguru can handle it
    logger.info(run_command("sudo apt update && sudo apt install -y usbip"))
    logger.info(run_command("sudo modprobe usbip-core && sudo modprobe usbip-host"))
    logger.info(run_command("sudo usbipd -D"))

    uvicorn.run(app, host="0.0.0.0", port=9135, log_config=None)