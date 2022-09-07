#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="USBIP Manager",
    version="0.1.0",
    description="Allows the usage of USBIP with a basic management frontend.",
    license="MIT",
    install_requires=[
        "fastapi == 0.63.0",
        "fastapi-versioning == 0.9.1",
        "loguru == 0.5.3",
        "pyserial == 3.5",
        "starlette == 0.13.6",
        "uvicorn == 0.13.4",
        "aiofiles == 0.6.0",
    ],
)