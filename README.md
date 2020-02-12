UrsaLeo LED Debug Board for Raspberry Pi Library
==

### Note

If your Raspberry Pi is already running the UrsaLeo Gateway Demo, stop the demo & led-manager services before running the example code.
```
sudo systemctl stop demo led-manager
```
To restart them after executing the examples:
```
sudo systemctl start demo led-manager
```
### Enable I2C
The board uses the I2C interface - enable this in raspi-config / interface options.
```
sudo raspi-config
```

### Installation
Download library from GitHub.

```
git clone https://github.com/UrsaLeo/LEDdebug.git
```

Install library.

```
cd LEDdebug
sudo pip3 install .
```

### Example code
LEDdebug/examples contains example code for use in your own Python clients.
```
cd LEDdebug/examples
```

**LED Demo**

Flashes the LED's then turns them on sequentially.

```
python3 led-demo.py
```

**Button Demo**

Flashes the LED's then waits for button presses on SW1 & SW2, turning LED1 & LED2 on and off respectively.
Ctl+C to exit
```
python3 button-demo.py
```

**Threaded Button Demo**

Flashes LED6 whilst waiting for button presses on SW1 & SW2 in a separate thread.
Ctl+C to exit
```
python3 threaded-button-demo.py
```

**LED Manager Service**

Runs a systemd service to monitor applications and processes. Code your applications or services to set and remove flags in /tmp when they start and stop. LED manager will indicate the status on the LED's configured in led-manager.service
```
sudo mkdir /usr/lib/led
sudo cp led-manager.py /usr/lib/led/
sudo cp led-manager.service /etc/systemd/system/
sudo cp led-manager.conf /usr/lib/tmpfiles.d/
sudo systemctl daemon-reload
sudo systemctl start led-manager
```

LED1 & 2 should now be blinking

Run the following command, LED1 will turn on:
```
touch /tmp/LED1
```

Run the following command, LED1 will blink:
```
rm /tmp/LED1
```
