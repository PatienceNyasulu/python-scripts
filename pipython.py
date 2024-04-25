import time
import paho.mqtt.client as mqtt
import ssl
import json
import thread
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='./AmazonRootCA1.pem', certfile='./ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-certificate.pem.crt', keyfile='./1ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("a3s1cqgu0ggloe-ats.iot.eu-central-1.amazonaws.com", 8883, 60) #Taken from REST API endpoint - Use your own. 


def intrusionDetector(Dummy):
    while (1):    
    x=GPIO.input(21)
        if (x==0): 
            print "Just Awesome" 
            client.publish("Device/data", payload="To the World NCT!!" , qos=0, retain=False)
        time.sleep(5)

thread.start_new_thread(intrusionDetector,("Create intrusion Thread",))
    
client.loop_forever()
