import colorsys
import json
import time
from datetime import datetime, timedelta
from os.path import exists

import requests
from dateutil import parser


class NetatmoHue:
    def __init__(
        self,
        _CLIENT_ID,
        _CLIENT_SECRET,
        _USERNAME,
        _PASSWORD,
        scope,
        _BASE_URL,
        _IP,
        _SETTINGS,
    ):
        self.clientId = _CLIENT_ID
        self.clientSecret = _CLIENT_SECRET
        self.username = _USERNAME
        self.password = _PASSWORD
        self._BASE_URL = "https://api.netatmo.com/"
        self._AUTH_REQ = _BASE_URL + "oauth2/token"
        self._AUTH_REFREH = _BASE_URL + "oauth2/token"
        self.scope = scope
        self.stationsData = ""
        self.usernameHue = ""
        self.ip = _IP
        self.settings = _SETTINGS

        response = requests.post(
            url=self._AUTH_REQ,
            data={
                "grant_type": "password",
                "client_id": self.clientId,
                "client_secret": self.clientSecret,
                "username": self.username,
                "password": self.password,
                "scope": self.scope,
            },
        )

        # Save json response as a variable
        self.netatmo_tokens = response.json()
        self.expiration = int(self.netatmo_tokens["expire_in"] + time.time())

    def accessToken(self) -> str:
        # use the refresh_token to get the new access_token
        if self.expiration < time.time():
            # Make Strava auth API call with current refresh token
            # print('token refreshed')
            response = requests.post(
                url=self._AUTH_REFREH,
                data={
                    "client_id": self.clientId,
                    "client_secret": self.clientSecret,
                    "grant_type": "refresh_token",
                    "refresh_token": self.netatmo_tokens["refresh_token"],
                },
            )

            self.netatmo_tokens = response.json()
            self.expiration = int(self.netatmo_tokens["expire_in"] + time.time())

        return self.netatmo_tokens["access_token"]

    def storeStationsData(self) -> str:
        endpoint = "https://api.netatmo.com/api/getstationsdata"
        headers = {
            "Authorization": f"Bearer {self.accessToken()}",
            "accept": "application/json",
        }
        self.stationsData = requests.get(endpoint, headers=headers).json()
        return "Station data retrieved"

    def getCO2(self, station, module=None):
        result = "Not Found"

        for dev in self.stationsData["body"]["devices"]:
            if dev["station_name"] == station:
                if module is not None:
                    for mod in dev["modules"]:
                        if mod["module_name"] == module:
                            result = mod["dashboard_data"]["CO2"]
                else:
                    result = dev["dashboard_data"]["CO2"]
        return result

    def connectToBridge(self, ip):
        response = requests.post(url=f"http://{ip}/api", json={"devicetype": "python"})
        resp = response.json()

        for line in resp:
            for key in line:
                if "success" in key:
                    with open("hue_config.json", "w") as out_file:
                        print("Successfully connected to the Bridge")
                        out_file.write(json.dumps({ip: line["success"]}))

                if "error" in key:
                    error_type = line["error"]["type"]
                    if error_type == 101:
                        print(
                            "The link button has not been pressed in the last 30 "
                            "seconds. Please press link button and wait 10 seconds "
                            "for this code to retrieve the username."
                        )
                        time.sleep(10)
                    if error_type == 7:
                        print("Unknown username")

    def get_usernameHue(self):
        if not self.usernameHue:
            filename = "hue_config.json"
            if exists(filename):
                try:
                    with open("hue_config.json") as f:
                        data = json.load(f)
                        self.usernameHue = data[self.ip]["username"]
                        # print(data)
                        # return data[self.ip]['username']

                except FileNotFoundError:
                    print(f"File Not Found: {filename}")

            else:
                self.connectToBridge(self.ip)
                self.get_usernameHue()

        return self.usernameHue

    def getHue(self, co2) -> int:
        x = ((co2 - 400) / 500) * 100
        if x < 80:
            g = 0
            r = 255 * (80 - x) / 80
            bl = 255  # * x/80
        if x >= 80:
            r = 0
            g = 255 * (x - 80) / 20
            bl = 255 - (255 * (x - 80) / 20)
        h, s, v = colorsys.rgb_to_hsv(r, g, bl)
        return int(round(h * 65535))

    def setHue(self, light, co2):
        response = requests.put(
            url=f"http://{self.ip}/api/{self.get_usernameHue()}/lights/{light}/state",
            json={"hue": self.getHue(co2), "on": True},
        )
        resp = response.json()  # noqa: F841
        # print(resp)

    def setLightByPPM(self, station, module, lights, sensor=None):
        if sensor is not None:
            # print('Sensor specified')
            s = self.getSensor(sensor)
            lu = s["state"]["lastupdated"]
            d = self.getTimeDiff(lu)
            if s["state"]["presence"] or d < 15:
                if module is not None:
                    co2 = self.getCO2(station, module)
                else:
                    co2 = self.getCO2(station)
                for light in lights:
                    self.setHue(light=light, co2=co2)
                    # print('light hue set because presence was detected')
        else:
            co2 = self.getCO2(station, module)
            for light in lights:
                self.setHue(light=light, co2=co2)
            # print('light hue set without sensor')

    def getSensor(self, sensor):
        response = requests.get(
            url=f"http://{self.ip}/api/{self.get_usernameHue()}/sensors/{sensor}"
        )
        return response.json()

    def getTimeDiff(self, lu) -> float:
        now = datetime.now() - timedelta(hours=2)
        yourdate = parser.parse(lu)
        return (now - yourdate).total_seconds() / 60

    def start(self):
        while True:
            for setting in self.settings.values():
                # print(setting['station'])
                self.storeStationsData()
                sensor = setting.get("sensor")
                module = setting.get("module")
                self.setLightByPPM(
                    station=setting["station"],
                    module=module,
                    light=setting["light"],
                    sensor=sensor,
                )
            time.sleep(300)
            # teller += 1
