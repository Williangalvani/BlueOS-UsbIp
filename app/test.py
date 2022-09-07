data = """ Exportable USB devices
======================
 - localhost
        2-1: PNY : unknown product (154b:00ed)
           : /sys/devices/platform/scb/fd500000.pcie/pci0000:00/0000:00:00.0/0000:01:00.0/usb2/2-1
           : (Defined at Interface level) (00/00/00)

      1-1.3: Silicon Labs : CP210x UART Bridge (10c4:ea60)
           : /sys/devices/platform/scb/fd500000.pcie/pci0000:00/0000:00:00.0/0000:01:00.0/usb1/1-1/1-1.3
           : (Defined at Interface level) (00/00/00)
"""


data = data.split("localhost")[1].strip().split("\n")
data = [line.strip() for line in data if line and "           : /" not in line and "           : (" not in line]
ids = [line.split(": ")[0] for line in data]
print(ids)