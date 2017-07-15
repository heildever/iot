import json
import random
import time
from datetime import datetime
from dweet import Dweet
import paho.mqtt.publish as publish
from weather_info import Weather
import urllib2

data = urllib2.urlopen("http://0.0.0.0:8080/config").read()
data = json.loads(data)


class Sensornode(Weather):
    def __init__(self, zone, node):
        Weather.__init__(self)
        self.configuration = data
        self.zone = zone
        self.node = node
        self.id = self.zone + "/" + self.node
        self.rise = self.getsunrise()
        self.set = self.getsunset()
        self.brokerIP = self.configuration['Parameters']['IP']
        self.port = self.configuration['Parameters']['port']
        self.timestamp = time.time()
        self.payload = self.gen_payload()
        self.lux = self.get_lux()
        self.occupation = self.get_motion()

    def get_lux(self):
        currenttime = datetime.now().strftime("%H.%M")
        sunrise = datetime.fromtimestamp(int(self.rise)).strftime("%H.%M")
        sunset = datetime.fromtimestamp(int(self.set)).strftime("%H.%M")
        if (currenttime >= sunrise) & (currenttime <= sunset):
            if (10 <= currenttime <= 14):
                self.lux = random.randint(3, 5)
            else:
                self.lux = random.randint(0, 3)
        else:
            self.lux = 0  # no more daylight
        return self.lux

    def get_motion(self):
        occupation = random.randint(0, 50)
        if occupation == 0:
            self.occupation = 1
        else:
            self.occupation = 0
        return self.occupation

    def gen_payload(self):
        self.payload = {"timestamp": self.timestamp, "lux": self.get_lux(), "pir": self.get_motion(), "DeviceID": self.id}
        return self.payload

    def publish(self):
        # publish.single("pir/"+"{}".format(self.id), json.dumps(self.payload), hostname=self.brokerIP)
        publish.single("lux/"+"{}".format(self.id), json.dumps(self.payload), hostname=self.brokerIP)

    def dweet(self):
        id = self.id.replace("/", "")
        Dweet.dweet_by_name(name="{}".format(id), data=self.payload)
