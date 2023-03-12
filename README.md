# RaspberryPi A
The file IOT-HW3-Raspberry Pi A has the following data:
- `main.py` - This is the MQTT client on RaspberryPi A which is both a subscriber and publisher.

## Objective
-  The LED2 connected to the Raspberry Pi B should turn on and turnoff when the Raspberry Pi A  status is online and offline respectively. Raspberry Pi A can go offline on both graceful and ungraceful disconnect.
- The values of potentiometer and LDR should be read and if either of the values being read is greater than threshold(chosen as 0.2) with respect to its previous values, then the values should be published. The LDR value should be published to the topic "lightSensor" and potentiometer value should be published to the topic "threshold". 

## Libraries used
- paho-mqtt (For establishing connection to the broker)
- Adafruit_MCP3008 (Library used for interfacing with MCP3008 ADC)

## How to run
-  Make sure you have the prerequisites described below before you start the experiment.

- Change the broker address from to the ip-address where the broker is hosted.

### Required installations
- Install paho- mqtt that we use for establishing a mqtt connection to the broker.
    ```
    pip3 install paho-mqtt
    ```
- Install Adafruit_MCP3008 that we use to interface with MCP3008 ADC.
    ```
    sudo pip3 install adafruit-mcp3008
    ```
### Prerequisites
#### Broker     
-   We used HiveMQ MQTT Broker. For our case, we downloaded the broker and ran it in the local machine. Broker should be running on Laptop 1 before starting the Raspberry Pi A for the connection to be created and for subcribing and publishing.

#### Raspberry Pi B
- Rapsberry Pi B should be running for subscribing to the values published by Rapsberry Pi A and lighting the LEDs accordingly.

### Raspberry Pi C
- This should be started to receive the LDR and potentiometer values published by Raspberry Pi A and send messages accordingly to Raspberry Pi B

#### Laptop2
- Laptop2 should be already if the log values are to be captured and the status of LED1 is to be printed.

### Run the Rapsberry Pi A demo
- For connecting Raspberry Pi A to the broker run:
    ```
    python3 main.py
    ```
- For gracefully disconnecting Raspberry Pi A:
    ```
    Ctrl + C - KeyBroardInterrupt
    ```
- For ungracefully disconnecting Raspberry Pi A:
    ```
    Disconnect Raspberry Pi A from wifi
    OR
    Turnoff the Laptop that runs Raspberry Pi A
    ```
## What happens in Raspberry Pi A
-   LWT (Last Will and Testament) is implemented using the will_set() method in the paho-mqtt library.
- Retain flag is set while publishing to the topics and while calling will_set() for retaining the messages published.
- The LDR value is read and decided if to be published based on the following:
    - The input for LDR is given to channel 0 and hence 0 is used in the function read_adc() to read the current LDR value.
    - The LDR value is normalized to be in between 0 and 1.
    - Previous LDR value is obtained by subscribing to the topic "lightSensor" within Raspberry Pi A.
    - Now that we have the current and previous values for LDR we can find the difference and if that is greater than the set threshold, the current LDR value is published to the topic "lightSensor".

- The Potentiometer value is read and decided if to be published based on the following: 
    - The input for potentiometer is given to channel 2 and hence 2 is used in the function read_adc() to read the current potentiometer value.
    - The potentiometer value is normalized to be in between 0 and 1.
    - Previous potentiometer value is obtained by subscribing to the topic "threshold" within Raspberry Pi A.
    - Now that we have the current and previous values for potentiometer we can find the difference and if that is greater than the set threshold, the current potentiometer value is published to the topic "threshold".
- For the Raspberry Pi A to sample the values of LDR and potentiometer every 100ms, a delay is introduced between successive reads by calling sleep(). This will set the sampling rate of ADC ro 10Hz.