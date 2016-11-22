#!/usr/bin/env python
# 50.012 Lab 9 skeleton script
# Nils, SUTD, 2016
# based on https://sakshambhatla.wordpress.com/2014/08/11/simple-mqtt-broker-and-client-in-python/
import paho.mqtt.client as mqtt

import cmd
import sys
import time
import select

username = "boohoo"
broker = "scy-phy.net"
port = 1337
dchannels = ['user/'+username, 'team/useless']

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
        if rc==mqtt.MQTT_ERR_SUCCESS:
                print("Connected successfully to %s"%broker)
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        for dc in dchannels:
                print("Subscribing to channel %s"%dc)
                # TODO: put code here to subscribe to channel
                client.subscribe(str(dc))
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Message received on topic: %s, using QoS %s\nMessage: %s"%(msg.topic,str(msg.qos),str(msg.payload)))

class cli(cmd.Cmd):
    """Simple MQTT chat client."""

    client = None
    looping = True

    def do_msg(self, line):
        "send hello message to user/<person>"
        try:
            info = (line.split(" ")[0], line.split(" ")[1:])
            person = info[0]
            greeting = " ".join(info[1])
        except:
            person = "anonymous"
            greeting = "hello %s"%(person)
        print("Sending %s to %s"%(greeting,"user/"+person))
        # TODO: put code here to publish to channel
        self.client.publish(topic='user/'+str(person), payload=greeting)

    def do_msgchannel(self, line):
        """ sends greeting to the channel"""
        try:
            info = (line.split(" ")[0], line.split(" ")[1:])
            channel=info[0]
            greeting = " ".join(info[1])
        except:
            channel="team/useless"
            greeting="master_lee"
        self.client.publish(topic=channel, payload=greeting)

    def do_quit(self, line):
            "Exit the MQTT client"
            print("Goodbye!")
            exit(0)

if __name__ == '__main__':

    client = mqtt.Client(username, clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    time.sleep(1)

    cli.client=client

    print("Welcome to the MQTT client CLI. Type 'help' or 'msg <person>'")
    # If there's input ready, do something, else do something
    # else. Note timeout is zero so select won't block at all.
    while True:
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = sys.stdin.readline()
                    if line:
                            cli().onecmd(line)
                    else: # an empty line means stdin has been closed
                            print('eof')
                            exit(0)
            else:
                    client.loop(1)

