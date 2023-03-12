import paho.mqtt.client as mqtt
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import sys

client = mqtt.Client(client_id="Pi-A")

prev_poten_value = 0
prev_ldr_value = 0
threshold = 0.2

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def on_connect(client, userdata, flags, rc): # Called when Raspberry Pi A is connected to the broker
    print("Connected with result code ", str(flags) , str(rc))
    client.publish("Status/RaspberryPiA" ,"online", qos=2, retain = True)
    client.subscribe("lightSensor", qos=2)
    client.subscribe("threshold", qos=2)

def on_disconnect(client, userdata,  rc): # Called when Raspberry Pi A is disconnected from the broker
    print("Disconnected with result code " + str(rc))

def on_message(client, userdata, msg): # Called when a new subscription is recieved.
    print(" published values", msg.topic, msg.payload)
    global prev_poten_value
    global prev_ldr_value
    if msg.topic == "threshold": # Publishes the potentiometer value
        prev_poten_value = float(msg.payload)
        print("recieved value:", float(msg.payload))
    if msg.topic == "lightSensor": # Publishes the LDR value
        prev_ldr_value = float(msg.payload)
      
def read_values():  
    while True:
        ldr_value = mcp.read_adc(0) # read LDR value
        potentiometer_value = mcp.read_adc(2) # read potentiometer value
        print("Potent",potentiometer_value)
        print("ldr",ldr_value)

        #normalize LDR and potentiometer to lie between 0 and 1
        ldr_value = (ldr_value - 30) / (1008 - 30) # ldr values output by ADC is in range 30 to 1008
        potentiometer_value = (potentiometer_value - 0) / 1023 # potentiometer values output by ADC is in range 0 to 1023

        #print("current Ldr =", ldr_value, " current potentiometer = ", potentiometer_value, " previous ldr = ", prev_ldr_value, " previous potentiometer = ", prev_poten_value)

        if abs(ldr_value - prev_ldr_value) > threshold or abs(potentiometer_value - prev_poten_value) > threshold:
            client.publish("threshold", potentiometer_value, qos=2, retain= True)
            client.publish("lightSensor", ldr_value, qos=2, retain= True)

        time.sleep(0.1) # ADC samples the values of LDR and potentiometer every 100ms
        
#Change the ip adress here to that of the machine running the broker
client.connect("169.254.180.48", 1883, 60)
client.will_set("Status/RaspberryPiA","offline",qos=2, retain = True)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

try:
    client.loop_start()
    read_values()
except KeyboardInterrupt:
    client.publish("Status/RaspberryPiA" ,"offline", qos=2, retain = True)
    client.disconnect() #disconnect message is called on KeyBoardInterrupt to mock graceful disconnect
    client.loop_stop()

# The commented out code below is to mock the changes for Raspberry Pi A from Laptop
# print("1. threshold= 0.5 LDR = 0.7 \n 2. threshold= 0.7 LDR = 0.5 \n 3. TurnOn \n 4. TurnOff \n 5. RaspberryPiA - online \n 6. RaspberryPiA - offline \n 7. RaspberryPiC - online \n 8. RaspberryPiC - offline \n 9.exit")

# while True:
#     status = input("Enter the option:")
#     status = int(status)
#     if status == 1:
#         client.publish("threshold", 0.5, qos=2)
#         client.publish("lightSensor", 0.7, qos=2)
#     if status == 2:
#         client.publish("threshold", 0.7, qos=2)
#         client.publish("lightSensor", 0.5, qos=2)
#     if status == 3:
#         print("yes")
#         client.publish("LightStatus", "TurnOn", qos=2)
#     if status == 4:
#         client.publish("LightStatus", "TurnOff", qos=2)
#     if status == 5:
#         client.publish("Status/RaspberryPiA", "online", qos=2)
#     if status == 6:
#         client.publish("Status/RaspberryPiA", "offline", qos=2)
#     if status == 7:
#         client.publish("Status/RaspberryPiC", "online", qos=2)
#     if status == 8:
#         client.publish("Status/RaspberryPiC", "offline", qos=2)
#     if status == 9:
#         break