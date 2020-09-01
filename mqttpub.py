# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:27:10 2019

@author: Swathi
"""

import paho.mqtt.client as mqtt
import time
 
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
        
def on_publish(client, obj, mid):
    print("mid: " + str(mid))#check the id
    pass
 
Connected = False   #global variable for the state of the connection
 
broker_address= "comp3310.ddns.net"  #Broker address
port = 1883                        #Broker port
user = "students"                    #Connection username
password = "33106331"
 
client = mqtt.Client("3310-u6439994",mqtt.MQTTv31) #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect 
client.on_publish = on_publish                     #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
print("publishing ")
(rc,mid)=client.publish("studentreport/u6439994/network","ANU Network",qos=2, retain=True)
print(rc)#check status
time.sleep(4)
client.disconnect() #disconnect
client.loop_stop() #stop loop