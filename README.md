# blade-id

This is a script to control the LEDs of [Uptime Lab](https://uplab.pro/) Compute Blade.
It's an extended version of the Example provided by Uptime Lab in the Compute Blade documentation.

It is still in an experimental stage.

## How to use

There are three files:

### blade-id.py

This is the script which runs in an endless loop and checks the temperature and load of the Compute Blade.
It set's the colors of the two RGB LEDs to a color between green and red depending on the temperature and load.
It also can let the front LED blink blue to ID a specific blade.
You can enable the ID feature by pressing the button or sending SIGUSR1 to the python process.

### blade-id.conf.example

This is an example configuration. The `blade-id.py` script expects a configuration in `/etc/blade-id.conf`.

### systemd/blade-id.service

This is an example systemd unit file to let to start/supervise the python script.
