from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

def helloworld(self, params, packet):
 print ('Recieved Message from AWS IoT Core')
 print ('Topic: '+ packet.topic)
 print ("Payload: ", (packet.payload))

myMQTTClient = AWSIoTMQTTClient ("raspberry") #random key, if anotier connection using the same key is
myMQTTClient.configureEndpoint("a3s1cqgu0ggloe-ats.iot.eu-central-1.amazonaws.com", 8883)

myMQTTClient. configureCredentials("AmazonRootCA1.pem", "ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-private.pem.key", "ab41d0a6fc44dea8cbdaf000498a154a78feddc4e0a17270d035dbddb642b8b8-certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing 
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 HZ 
myMQTTClient.configureConnectDisconnectTimeout (10) # 10 sec
myMQTTClient.configureMQTTOperationTimeout (5) # 5 sec
print ('Initiating IoT Core Topic ... ') 
myMQTTClient.connect ( )
#myMQTTClient.subscribe("home/helloworld", 1, helloworld)

#while True:
 #   time.sleep(5)
print("Publishing message from RPI")
myMQTTClint.publish(
    topic="home/helloworld",
    Qos=1
    payload="{'Message' : 'Message by RPI'}")
