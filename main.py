import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #client.publish("Status/RaspberryPiA" ,"online", qos=2)

def on_disconnect(client, userdata,  rc):
    print("Disconnected")
    #client.publish("Status/RaspberryPiA" ,"offline", qos=2)


client = mqtt.Client(client_id="publisher") #, lastWillTopic = "Status/RaspberryPiA", lastWillQos = 2, lastWillMessage = "offline", lastWillRetain = True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect("192.168.0.191", 1883, 60)

#client.loop_forever()

print("1. threshold= 0.5 LDR = 0.7 \n 2. threshold= 0.7 LDR = 0.5 \n 3. TurnOn \n 4. TurnOff \n 5. RaspberryPiA - online \n 6. RaspberryPiA - offline \n 7. RaspberryPiC - online \n 8. RaspberryPiC - offline \n 9.exit")

while True:
    status = input("Enter the option:")
    status = int(status)
    if status == 1:
        client.publish("threshold" ,0.5, qos=2)
        client.publish("lightSensor" ,0.7, qos=2)
    if status == 2:
        client.publish("threshold" ,0.7, qos=2)
        client.publish("lightSensor" ,0.5, qos=2)
    if status == 3:
        print("yes")
        client.publish("LightStatus" ,"TurnOn", qos=2)
    if status == 4:
        client.publish("LightStatus" ,"TurnOff", qos=2)
    if status == 5:
        client.publish("Status/RaspberryPiA" ,"online", qos=2)
    if status == 6:
        client.publish("Status/RaspberryPiA" ,"offline", qos=2)
    if status == 7:
        client.publish("Status/RaspberryPiC" ,"online", qos=2)
    if status == 8:
        client.publish("Status/RaspberryPiC" ,"offline", qos=2)
    if status == 9:
        break

client.disconnect()


