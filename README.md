# iot
This repository it contains the python modules explained below. The modules are pieces of a user-centric smart lighthing mechanism and they are meant to work together with a decision algorithm - can be found [here](https://github.com/hobyfrezk/IOT-smart-office-light-system).

## Getting Started 
Please make sure you clone both repo's and setup an MQTT broker on the LAN. 

### Modules
- **weatherinfo.py** fetches weather related data (weather, sunrise etc) about Turin, Italy from OpenWeatherMap's API
- **dweet.py** contains a Class for using the Dweet.io servers for data communication between devices
- **sensornode.py** is a simulated PIR sensor
- **switch.py** launches an HTML web interface to control the system configuration which then modifies **config.json**
- **pub_init.py** initiates publishing & dweeting messages to the MQTT broker

### Built With
* [CherryPy](https://github.com/cherrypy/cherrypy) - a pythonic, object-oriented HTTP framework
* [Eclipse Mosquitto](https://github.com/eclipse/mosquitto) - an open source MQTT broker
* We used a Raspberry Pi to control the switches and real sensors but it's *optional*

## License 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\
This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details. 
