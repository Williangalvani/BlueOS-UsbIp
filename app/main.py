#! /usr/bin/env python3
import logging
import shutil
import subprocess
import time
from enum import Enum
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi_versioning import VersionedFastAPI, version
from fastapi.staticfiles import StaticFiles
from loguru import logger

SERVICE_NAME = "UsbIpManager"

user = "pi"
password = "raspberry"

def run_command(command: str, check: bool = True) -> "subprocess.CompletedProcess['str']":

    return subprocess.run(
    [
        "sshpass",
        "-p",
        password,
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        f"{user}@localhost",
        command,
    ],
    check=check,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)


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
    output = run_command(command).stdout.strip()
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
    output = run_command(command).stdout.strip()
    try:
        data = output.split("localhost")[1].strip().split("\n")
        data = [line.strip() for line in data if line and "           : /" not in line and "           : (" not in line]
        ids = [line.split(": ")[0] for line in data]

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
    output = run_command(command).stdout
    return output


@app.post("/command/unbind", status_code=status.HTTP_200_OK)
@version(1, 0)
async def command_unbind(device: str) -> Any:
    command = f'sudo usbip unbind -b {device}'
    logger.debug(f"Running command: {command}")
    output = run_command(command).stdout
    return output


app = VersionedFastAPI(app, version="1.0.0", prefix_format="/v{major}.{minor}", enable_latest=True)

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Running uvicorn with log disabled so loguru can handle it
    logger.info(run_command("sudo modprobe usbip-core && sudo modprobe usbip-host"))
    logger.info(run_command("sudo usbipd -D"))

    uvicorn.run(app, host="0.0.0.0", port=9135, log_config=None)