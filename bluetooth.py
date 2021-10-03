import asyncio
from bleak import BleakScanner
import json
import requests
prev = []

def printer(theList):
    for element in theList:
        print(element)


async def run():
    global prev
    global pop
    devices = await BleakScanner.discover()

    delta = (len(devices)-len(prev) ) 
    temp = devices
    newList = []
    for device in devices:
        newList.append({"address": device.address,"rssi": device.rssi})

    #print(newList)

    
    print("dif", delta)
    print("old", len(prev))
    print("new", len(devices))

    prev = temp
    myDict = {"dif": delta,"old":len(prev),"new": len(devices),"devices":newList}
    jsonString = json.dumps(myDict)
    dataRaw = requests.post("https://roomify.electrokid.co.uk/api/devices", headers = {"key": "roomify123", "roomid":'1'},data = jsonString)
    print(dataRaw.text)
    


    
while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


