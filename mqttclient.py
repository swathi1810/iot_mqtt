#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: u6439994
"""
import paho.mqtt.client as mqtt
import time
import statistics

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    global Connected                #Use global variable
    Connected = True
    client.subscribe(("counter/fast/q2",2))
 
    #client.subscribe("$SYS/broker/load/bytes/sent/1min")
    #client.subscribe("$SYS/broker/load/messages/received/1min")
   
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global number
    global list1
    global dict_val
    global elapsed_time
    global time_gap
    number+=1
    list1.append(str(msg.payload))
    time_gap.append(elapsed_time)
    if(str(msg.payload) not in dict_val):
        dict_val[str(msg.payload)]=1
    else:
        dict_val[str(msg.payload)]+=1
    print(msg.topic+" "+str(msg.payload))
    
'''extracts the message converts into integer and checks for lost messages if the difference between two consecutive values is
greater than 1 then its supposed that the messages are lost'''    
def convert_count(list_message):
    global num
    global list2
    diff=[]
    tot=[]
    for str1 in list_message:
        try:
            list2.append(int(str1[2:(len(str1)-1)]))
        except:
            continue
    #print(list2)
    for i in range(0,len(list2)):
        if(list2.index(list2[i])==(len(list2)-1)):
            break
        else:
            diff.append((list2[i+1]-list2[i]))
    #print(diff)
    for s in diff:
        if(s>1):
            tot.append(s)
            num.append(list2[diff.index(s)])
            num.append(list2[diff.index(s)+1])
    return tot
def cal_mean_time(time_g):
    mean_diff=[]
    for i in range(0,len(time_g)):
        if(i==(len(time_g)-1)):
            break
        mean_diff.append((time_g[i+1]-time_g[i])*1000)
    return(mean_diff)
    
'''checks for out of order messages if the difference between two consecutive values is
less than 1 then its supposed that the messages are order of order''' 
def count_outoforder():
    global list2
    diff=[]
    tot=[]
    for i in range(0,len(list2)):
        if(list2.index(list2[i])==(len(list2)-1)):
            break
        else:
            diff.append((list2[i+1]-list2[i]))
    #print(diff)
    for s in diff:
        if(s<1):
            tot.append(s)
            num.append(list2[diff.index(s)])
            num.append(list2[diff.index(s)+1])
    return tot
    
    
    
broker_address= "comp3310.ddns.net"  #Broker address
port = 1883                        #Broker port
user = "students"                    #Connection username
password = "33106331"
#some global variables
number=0
list1=[]#payload is stored
num=[]
list2=[]#integer payload
dict_val={}
get_val={}
time_gap=[]#difference in time betwwen two messages
global_dict={}
list_list=[]#stores all the intermediate values
dup_list=[]#stores all the duplicate values
client = mqtt.Client("3310-u6439994",mqtt.MQTTv31)
client.username_pw_set(user, password=password)
client.on_connect = on_connect

client.on_message = on_message
client.connect(broker_address, port=port)
client.loop_start()
#time since the loop started
start_time = time.time()
elapsed_time = time.time() - start_time
try:
    #listens for 5 minutes 
    while (elapsed_time<=60):
        elapsed_time = time.time() - start_time
        
    raise
 
except:
    print ("exiting")#after 5 minutes it disconnects
    print(number)
    client.disconnect()#some messages gets delivered before disconnecting in that milliseconds tme frame
    client.loop_stop()
    sum_loss=convert_count(list1)#calling the func for lost messages
    sum_out_of_order=count_outoforder()#calling the function for our of order messages 
    for key in dict_val:
        if(dict_val[key]>1):
            #print(key,dict_val[key])
            dup_list.append(dict_val[key]-1)
    #print(num)
    print(len(list1)/300)
    list_list.append(len(list1)/300)
    list_list.append(sum(sum_loss))
    list_list.append(sum(dup_list))
    list_list.append(sum(sum_out_of_order))
    mean_time=cal_mean_time(time_gap)
    #print(time_gap)
    print(statistics.mean(mean_time))
    list_list.append(statistics.mean(mean_time))
    print(statistics.stdev(mean_time))
    list_list.append(statistics.stdev(mean_time))
    if 'counter/fast/q2' not in global_dict:
        global_dict['counter/fast/q2']=list_list
    print(global_dict['counter/fast/q2'])#shows all the five statistics


