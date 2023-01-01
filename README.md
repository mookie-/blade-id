# blade-id

This is a script to control the LEDs of [Uptime Lab](https://uplab.pro/) Compute Blade.
It's an extended version of the Example provided by Uptime Lab in the Compute Blade documentation.
It's a fork of [merocle](https://github.com/merocle) code examples from [this repository](https://github.com/merocle/FanUnit).

It is still in an experimental stage.

## Installation

### Dependencies

You need to install `python3-pip`:

```
sudo apt-get install python3-pip
```

and then [install the NeoPixel Library](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage):

```
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

As of 29th December 2022, if your Raspberry PI CM4 is newer (e.g. `Compute Module 4 Rev 1.1` from `cat /proc/cpuinfo`)
you will probably get this error:

```
RuntimeError: ws2811_init failed with code -3 (Hardware revision is not supported)
```

Then you will need to build `rpi_ws281x` yourself, see [this Github Issue](https://github.com/rpi-ws281x/rpi-ws281x-python/issues/56#issuecomment-753320723).

### APT-Repository

Currently only Raspbian/Debian bullseye is supported by the APT-Repository.

```
# setup apt-source
echo 'deb http://apt.bob.systems/blade-id/ bullseye main' > /etc/apt/sources.list.d/blade-id.list
# install gpg key
cd /etc/apt/trusted.gpg.d/
wget https://apt.bob.systems/blade-id/bob.systems-bladeid.gpg
# install blade-id
apt update
apt install blade-id
```

### Manual install/usage

You can use it and set it up manually if you want.
You will need to also install `python3-psutil`.

### blade-id

This is the script which runs in an endless loop and checks the temperature and load of the Compute Blade.
It set's the colors of the two RGB LEDs to a color between green and red depending on the temperature and load.
It also can let the front LED blink blue to ID a specific blade.
You can enable the ID feature by pressing the button or sending SIGUSR1 to the python process.
You can disable the ID feature by pressing the button or sending SIGUSR2 to the python process.

### blade-id.conf

This is an example configuration. The `blade-id` script expects a configuration in `/etc/blade-id.conf`.
If the configuration does not exist, it will use default values.

### systemd/blade-id.service

This is an example systemd unit file to let to start/supervise the python script.
