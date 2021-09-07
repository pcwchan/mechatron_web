import serial
import time
import string
import pynmea2
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException


pnChannel = "raspi-tracker"

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-9e6a038c-fe4e-11eb-b684-a2ddbe22cd06'
pnconfig.publish_key = 'pub-c-8bbb1243-efb1-4b95-8996-5d77d03b0864'
pnconfig.ssl = False
 
pubnub = PubNub(pnconfig)
pubnub.subscribe().channels(pnChannel).execute()


while True:
    port="/dev/ttyUSB0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()
    newdata=ser.readline()
    # print(ne)
    
    if newdata[0:6] == "$GPRMC"or newdata[0:4] == "GPVTG"or newdata[0:4] == "GPGGA"or newdata[0:4] == "GPGSA"or newdata[0:4] == "GPGLL" :
    
        newmsg=pynmea2.parse(newdata)	
        lat=newmsg.latitude
        lng=newmsg.longitude

        # gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
        try:
            envelope = pubnub.publish().channel(pnChannel).message({
            # 'lat':lat,
            # 'lng':lng
            }).sync()
            print("publish timetoken: %d" % envelope.result.timetoken)
            gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
            print(gps)

        except PubNubException as e:
            handle_exception(e)

