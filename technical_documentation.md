# Introduction

This document explains the code in pyNetatmoHue. 

## Structure 

The following functions are part of the module:

> **Init**: Authenticates the Netatmo API User

> **acessToken**: Refreshes the Netatmo token when its expired, else it used the already stored token. 

> **storeStationsData**: Retrieves and stores the Station data in an instance attribute. 

> **getCO2**: Retrieves the CO2 / PPM level for a given station (and module) by using the data that was retrieved and stored by *storeStationsData*.

> **connectToBridge**: Attempts to connect to the bridge. When the button has not been pressed, an error will be returned. When this happens an error message is printed asking to press the button. After 10 seconds this function will continue. 

> **get_usernameHue**: Returns the Hue Username, provided by the Hue bridge. If the instance variable is empty, the json file is read, if this is empty a connection to the bridge is attempted to retrieve the username.

> **getHue**: Returns a Hue value based on the measured CO2 / PPM level. A hard coded range of 400 to 900 PPM is used. Untill 80% of this range (untill 800 PPM), the amount of red changes. For the range 800 - 900 PPM the amount of green and blue change. 

> **setHue**: Sets the colour of the light by PPM / CO2 level. Uses getHue to calculate the amount of Hue per PPM level.

> **setLightByPPM**: For a given configuration (combination of station/module, light and sensor), sets the Hue level for light by PPM level, in case motion has been deteced in the last 15 minutes.  

> **getSensor**: Returns the sensor readings. 

> **getTimeDiff**: Returns the time difference in minutes from the provided datetime and now. 

> **start**: Infinite loop that sets the lights every 5 minutes by using the provided configurations (settings).  


