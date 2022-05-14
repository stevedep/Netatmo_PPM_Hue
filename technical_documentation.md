# Introduction

This document explains the code in pyNetatmoHue. 

## Structure 

The following functions are part of the module:

> **Init**: Authenticates the Netatmo API User

> **acessToken**: Refreshes the Netatmo token when its expired, else it used the already stored token. 

> **storeStationsData**: retreives and stores the Station data in a instance attribute. 

> **getCO2**: retreives the CO2 / PPM level for a given station (and module) by using the data that was retreived and stored by *storeStationsData*.



