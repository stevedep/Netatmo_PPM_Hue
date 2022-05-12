# pyNetatmoHue

This repository contains the module 'pyNetatmoHue.py' (Python code) that allows you to continuously automatically adjust the colours of your Hue lights according to the measured PPM levels by your Netatmo weather station. 

This is usefull when you want to easily monitor the PPM level in your room so you known when you need to ventilate your room (additionally). 

You can speficy a Netatmo Station and Module to measure the PPM level, a Hue light that will colour as the PPM level changes and a motion sensor (optional) that check if anybody is present in the room, if not, that light will not change colour. 

#### Target Audience
This repository is intended for (Python) Developers who would like to use this code, or ideally, would like to contribute.


## Installation

Install via PIP with:

    sudo pip install pyNetatmoHue

Use in Python like this:

``` 
import pyNetatmoHue as pNH

NH2 = pNH.NetatmoHue(
    _CLIENT_ID     = "xx",
    _CLIENT_SECRET = "xxx",
    _USERNAME      = "xx.xx@gmail.com",
    _PASSWORD      = "xx%xx*",
    scope="read_station read_camera access_camera write_camera " \
                                 "read_presence access_presence write_presence read_thermostat write_thermostat",
    _BASE_URL = "https://api.netatmo.com/",
    _IP = '192.168.2.7',
    _SETTINGS = {
    "portaal" : {"station": "_ (Keuken)", "module" : "Portaal", "light":[8], "sensor":16 },
    "werkkamer" : {"station" : "_ (Pepijn)", "module" : "Werkkamer", "light":[6], "sensor":160 },
    "keuken" : {"station" : "_ (Keuken)", "light":[3,4] }
       }
)

NH2.start()
 
```` 

#### API Credentials

Netatmo API credentials can be created via https://dev.netatmo.com/apps/. Register an APP to get a ClientID and Client Secret. 

#### Configuration

When you intitiate a class instance a number of parameter values are required. The following paramters are required to obtain the CO2 levels:
* _CLIENT_ID
* _CLIENT_SECRET
* _USERNAME     
* _PASSWORD   
* scope
* _BASE_URL

You also need to specify the IP adress of your HUE bridge. This is done using the parameter *_IP*. You can find you IP adres by using your HUE app and going to 'Settings' -> 'Hue Bridges' -> 'Information Icon'.

##### Settings 
The settings parameter consists of a nested dictionary with the rooms that each have a station or optionally also a module to retrevieve the CO2 level. The light(s) that need to be coloured in that room are specified (in a list). Finally, optionally, you can specify a motion sensor that checks for presence in the room. 

To obtain the light and sensor identifiers, I recommend the app 'all 4 hue'. In this app you can select a light or sensor and then choose 'show internal identifier'
