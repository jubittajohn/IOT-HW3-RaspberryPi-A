import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import time

prev_poten_value = 0
prev_ldr_value = 0
threshold = 0.1

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.publish("Status/RaspberryPiA" ,"online", qos=2, retain = True)
    client.subscribe("lightSensor", qos=2)
    client.subscribe("threshold", qos=2)

def on_disconnect(client, userdata,  rc):
    print("Disconnected")
    client.publish("Status/RaspberryPiA" ,"offline", qos=2, retain = True)

def on_message(client, userdata, msg):
    global prev_poten_value
    global prev_ldr_value
    if msg.topic == "threshold":
        prev_poten_value = msg.payload
    if msg.topic == "lightSensor":
        prev_ldr_value = msg.payload
        
client = mqtt.Client(client_id="publisher")
client.will_set("Status/RaspberryPiA","offline",qos=2, retain = True)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect("192.168.0.191", 1883, 60)

ldr_pin = 16  # ADC channel number for LDR
potentiometer_pin = 18  # ADC channel number for potentiometer

GPIO.setmode(GPIO.BOARD)
GPIO.setup(ldr_pin, GPIO.OUT)
GPIO.setup(potentiometer_pin, GPIO.OUT)

while True:
    try :
        ldr_value = GPIO.input(ldr_pin) # read LDR value
        potentiometer_value = GPIO.input(potentiometer_pin) # read potentiometer value

        #normalize LDR and potentiometer to lie between 0 and 1
        ldr_value = (ldr_value - 10) / 90 # ldr values output by ADC is in range 10 to 100
        potentiometer_value = (potentiometer_value - 90) / 160 # potentiometer values output by ADC is in range 90 to 250

        if (ldr_value - prev_ldr_value) > threshold or (potentiometer_value - prev_poten_value) > threshold:
            client.publish("threshold", potentiometer_value, qos=2, retain= True)
            client.publish("lightSensor", ldr_value, qos=2, retain= True)

        time.sleep(0.001)

    except KeyboardInterrupt:
        GPIO.cleanup()

#client.loop_forever()
'''
print("1. threshold= 0.5 LDR = 0.7 \n 2. threshold= 0.7 LDR = 0.5 \n 3. TurnOn \n 4. TurnOff \n 5. RaspberryPiA - online \n 6. RaspberryPiA - offline \n 7. RaspberryPiC - online \n 8. RaspberryPiC - offline \n 9.exit")

while True:
    status = input("Enter the option:")
    status = int(status)
    if status == 1:
        client.publish("threshold", 0.5, qos=2)
        client.publish("lightSensor", 0.7, qos=2)
    if status == 2:
        client.publish("threshold", 0.7, qos=2)
        client.publish("lightSensor", 0.5, qos=2)
    if status == 3:
        print("yes")
        client.publish("LightStatus", "TurnOn", qos=2)
    if status == 4:
        client.publish("LightStatus", "TurnOff", qos=2)
    if status == 5:
        client.publish("Status/RaspberryPiA", "online", qos=2)
    if status == 6:
        client.publish("Status/RaspberryPiA", "offline", qos=2)
    if status == 7:
        client.publish("Status/RaspberryPiC", "online", qos=2)
    if status == 8:
        client.publish("Status/RaspberryPiC", "offline", qos=2)
    if status == 9:
        break
'''

client.disconnect()


