import json
import os
import time

import cherrypy
import paho.mqtt.publish as publish

from dweet import Dweet

with open('config.json') as data_file:
    data = json.load(data_file)


class Gui(object):
    title = "Control panel of the lighting system\n"
    message = "Active nodes of the system : \n"
    configuration = data
    actives = data["DeviceID"]
    brokerIP = configuration['Parameters']['IP']
    timestamp = time.time()
    payload = {}
    id = ""
    # default values of mode and brightness
    mode = 1
    brightness = 5

    @cherrypy.expose
    def index(self):
        return """
                <html><head><body>
                    <title>%s</title>
                    <h1>%s</h1>
                    <p><mark>%s</mark></p>
               </body></head></html>
            """ % (self.title, self.title, self.message) + self.get_actives() + self.buttons()

    def get_actives(self):
        actives = self.actives
        return """
                <html><head><body>
                <ul>%s</ul>
                </body></head></html>
            """ % json.dumps(actives)

    @staticmethod
    def buttons():
        return """
                <html><head><body>
                    <form action="modify_node">
                        <b><br> Please select a zone and a node number to modify<br/></b>
                        <i><br> For example : zone4, node1</br></i>
                        zone :<input type="number" name="zone"><br>
                        node :<input type="number" name="node"><br><br>
                        <button type="submit" name="action" value="1">Add the node </button>
                        <button type="submit" name="action" value="0"> Remove the node</button>                    
                    </form>
                    <p><br><mark> Operation mode of the node </mark><br/></p>
                    <b>Please select a zone and a node number to select its mode</b>
                    <form action="modeselect">
                        zone :<input type="number" name="zone"><br>
                        node :<input type="number" name="node"><br><br>
                        <button type="submit" name="mode" value="1">AUTO </button>
                        <button type="submit" name="mode" value="0"> MANU</button> 
                    </form>
                </body></head></html>
            """

    @cherrypy.expose
    def modeselect(self, zone, node, mode):
        if "zone" + zone not in self.actives:
            return "The selected node does not exist, please select a new one" + self.index()
        self.id = "zone" + zone + "/" + "node" + node
        if int(mode) == 1:  # auto mode
            self.payload = {"timestamp": self.timestamp, "mode": '5', "DeviceID": self.id}
            publish.single("switch/" + self.id, json.dumps(self.payload), hostname=self.brokerIP)
            name = self.id.replace("/", "")
            name = self.id + "S"
            Dweet.dweet_by_name(name="{}".format(name), data=self.payload)
            return """ The selected node will be run on AUTO mode""" + self.index()
        else:  # manu mode
            return """
                <html><head><body>
                    <p><br> Please select a brightness level <br/></p>
                    <form action="final">
                        <button type="submit" value="0" name="bright"> 0</button>
                        <button type="submit" value="1" name="bright"> 1</button>
                        <button type="submit" value="2" name="bright"> 2</button>
                        <button type="submit" value="3" name="bright"> 3</button>
                        <button type="submit" value="4" name="bright"> 4</button>
                    </form>
                </body></head></html>
            """

    @cherrypy.expose
    def modify_node(self, zone, node, action):
        zone = "zone" + zone
        node = "node" + node
        if "{}".format(zone) in self.actives:
            if "{}".format(node) in self.actives["{}".format(zone)]:
                if int(action) == 1:
                    return "The selected node already exist, please select a new one" + self.index()
                else:
                    lista = self.actives["{}".format(zone)]
                    if len(lista) == 1:
                        del self.actives["{}".format(zone)]
                    else:
                        lista.remove("{}".format(node))
                        self.actives.update({"{}".format(zone): lista})
                    return self.modify_json()
            else:
                if int(action) == 1:
                    lista = self.actives["{}".format(zone)]
                    lista.append(node)
                    self.actives.update({"{}".format(zone): lista})
                    return self.modify_json()
                else:
                    return "The selected node does not exist, please select a new one" + self.index()
        else:
            if int(action) == 1:
                lista = [node]
                self.actives.update({"{}".format(zone): lista})
                return self.modify_json()
            else:
                return "The selected node does not exist, please select a new one" + self.index()

    def modify_json(self):
        time.sleep(3)
        payload = {"timestamp": self.timestamp, "config": "changed"}
        publish.single("config" + self.id, json.dumps(payload), hostname=self.brokerIP)
        os.remove('config.json')
        with open('config.json', 'w') as df:
            json.dump(data, df)
        return "Selected action is executed" + self.index()

    @cherrypy.expose
    def final(self, bright):
        self.payload = {"timestamp": self.timestamp, "mode": bright, "DeviceID": self.id}
        publish.single("switch/" + self.id, json.dumps(self.payload), hostname=self.brokerIP)
        name = self.id.replace("/", "")
        name = name + "S"
        Dweet.dweet_by_name(name="{}".format(name), data=self.payload)
        return """ The selected node will run on MANU mode with brightness : %s """ % bright + self.index()

    @cherrypy.expose()
    def config(self):
        df = open('config.json', 'r')
        return df

if __name__ == "__main__":
    cherrypy.config.update({
        'server.socket_host': data["Parameters"]["WSIP"],
        'server.socket_port': data["Parameters"]["WSPort"],
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True}
    })
    cherrypy.tree.mount(Gui(), '/')
    cherrypy.engine.start()
    cherrypy.engine.block()
