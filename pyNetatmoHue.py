import requests
import json
import time
from datetime import datetime, timedelta
from dateutil import parser
from os.path import exists
import colorsys

class NetatmoHue:
    def __init__(self, _CLIENT_ID, _CLIENT_SECRET, _USERNAME, _PASSWORD, scope, _BASE_URL, _IP, _SETTINGS):
        self.clientId=_CLIENT_ID
        self.clientSecret=_CLIENT_SECRET
        self.username=_USERNAME
        self.password=_PASSWORD
        self._BASE_URL = "https://api.netatmo.com/"
        self._AUTH_REQ = _BASE_URL + "oauth2/token"
        self._AUTH_REFREH = _BASE_URL + "oauth2/token"        
        self.scope = scope
        self.stationsData = ""
        self.usernameHue = ""
        self.ip = _IP
        self.settings = _SETTINGS
   
        response = requests.post(
                            url = self._AUTH_REQ,
                            data =  {
                        "grant_type" : "password",
                        "client_id" : self.clientId,
                        "client_secret" : self.clientSecret,
                        "username" : self.username,
                        "password" : self.password,
                        "scope" : self.scope
                        })

        #Save json response as a variable
        self.netatmo_tokens = response.json()
        self.expiration = int(self.netatmo_tokens['expire_in'] + time.time())
    
    def accessToken(self):
        # use the refresh_token to get the new access_token
        if self.expiration < time.time():
        # Make Strava auth API call with current refresh token
            #print('token refreshed')
            response = requests.post(
                                url = self._AUTH_REFREH,
                                data = {
                                        'client_id': self.clientId,
                                        'client_secret': self.clientSecret,
                                        'grant_type': 'refresh_token',
                                        'refresh_token': self.netatmo_tokens['refresh_token']
                                        }
                            )
        
            self.netatmo_tokens = response.json()
            self.expiration = int(self.netatmo_tokens['expire_in'] + time.time())
    
        return (self.netatmo_tokens["access_token"])
    
    def storeStationsData(self):
        endpoint = "https://api.netatmo.com/api/getstationsdata"
        headers = {"Authorization": "Bearer " + self.accessToken(),
                  "accept": "application/json"}
        self.stationsData = requests.get(endpoint, headers=headers).json()
        return 'Stationsdata retreived'
    
    def getCO2(self,station, module = None):
        result = 'Not Found'

        for dev in self.stationsData['body']['devices']:
            if dev['station_name'] == station:
                if module is not None:
                    for mod in dev['modules']:
                        if mod['module_name'] == module:
                            result = mod['dashboard_data']['CO2']
                else:
                    result = dev['dashboard_data']['CO2']
        return result
    
    def connectToBridge(self,ip):        
            response = requests.post(
                                url = 'http://' + ip + '/api',
                                json = {"devicetype": "python"}
                            )
            resp = response.json()

            
            for line in resp:
                for key in line:
                    if 'success' in key:
                        with open('hue_config.json', 'w') as f:                   
                            print('Successfully connected to the Bridge')
                            f.write(json.dumps({ip: line['success']}))                       

                    if 'error' in key:
                        error_type = line['error']['type']
                        if error_type == 101:
                            print('The link button has not been pressed in the last 30 seconds. Please press link button and wait 10 seconds for this code to retreive the username.')
                            time.sleep(10)
                        if error_type == 7:
                            print('Unknown username')
    
    def get_usernameHue(self):
        if self.usernameHue == '':
            file_exists = exists('hue_config.json')
            if file_exists:
                try:
                    with open('hue_config.json') as f:
                        data = json.load(f)
                        self.usernameHue = data[self.ip]['username']
                        #print(data)  
                        #return data[self.ip]['username']
                      
                except FileNotFoundError:
                    print('File Not Found')

                
            else:
                self.connectToBridge(self.ip)
                self.get_usernameHue()
        
        return self.usernameHue
    
    def getHue(self, co2):
        x = ((((co2-400)/500)*100))
        if x < 80:
            g = 0
            r = 255 * (80-x)/80 
            bl = 255 # * x/80
        if x >= 80:
            r = 0
            g = 255 * (x-80)/20
            bl = 255 - (255 * (x-80)/20)
        h, s, v = colorsys.rgb_to_hsv(r, g, bl)
        return int(round(h * 65535))
    
    def setHue(self, light, co2):
        response = requests.put(
                            url = 'http://' + self.ip + '/api/'+ self.get_usernameHue() + '/lights/' + str(light) + '/state',
                            json = {"hue": self.getHue(co2), "on" : True }
                        )
        resp = response.json()
        #print(resp)
    
    def setLightByPPM(self, station, module, light, sensor = None):
        if sensor is not None:
            #print('Sensor specified')
            s = self.getSensor(sensor)
            lu =  s['state']['lastupdated']
            d = self.getTimeDiff(lu)
            if s['state']['presence'] == True or d < 15:                   
                if module is not None:
                    co2 = self.getCO2(station, module)    
                else:
                    co2 = self.getCO2(station)
                for l in light:
                    self.setHue(light=l, co2=co2)
                    #print('light hue set because presence was detected')
        else:
            co2 = self.getCO2(station, module)    
            for l in light:
                    self.setHue(light=l, co2=co2)            
            #print('light hue set without sensor')
    
    def getSensor(self,sensor):
        un = self.get_usernameHue()
        #print(un)
        response = requests.get(
                            url = 'http://' + self.ip + '/api/'+ un + '/sensors/' + str(sensor) 
                        )
        resp = response.json()
        return resp 
    
    def getTimeDiff(self,lu):
        now = datetime.now() - timedelta(hours=2)
        yourdate = parser.parse(lu)
        c = (now - yourdate)
        d = c.total_seconds() / 60
        return d
    
    def start(self):
        
        while 1==1:        
            for settingname, setting in self.settings.items():
                #print(setting['station'])  
                self.storeStationsData()  
                sensor = setting['sensor'] if "sensor" in setting  else None
                module = setting['module'] if "module" in setting  else None
                self.setLightByPPM(station=setting['station'], module = module, light=setting['light'], sensor= sensor)
            time.sleep(300)  
            #teller += 1