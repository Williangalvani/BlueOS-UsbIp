# USB/IP extension

This exposes usb devices via IP, which can be used in another client device

# Client

## Linux:


```
# load modules
sudo modprobe usbip-core
sudo modprobe vhci-hcd
# list devices
sudo usbip list --remote blueos.local
# connect to device with bus 1-1.3
sudo usbip attach --remote blueos.local --busid 1-1.3

```

## Windows

Download the 3.6 dev release from https://github.com/cezanne/usbip-win and follow the "Client" instructions there.
The new "ude" driver seemed to work for me.