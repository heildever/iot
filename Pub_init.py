import time
import urllib2
import json
from Sensornode import Sensornode

while True:
    data = urllib2.urlopen("http://0.0.0.0:8080/config").read()
    data = json.loads(data)
    for zone, node in data["DeviceID"].iteritems():
        for node in node:
            l = Sensornode(zone, node)
            l.zone = zone
            l.node = node
            l.publish()
            l.dweet()
            time.sleep(5)
