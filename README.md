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
