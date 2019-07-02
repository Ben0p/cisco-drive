import json
import requests
import time

locations = 'http://10.221.247.237:8080/api/machineUCC/locations?timePreviousQuery=-1'

session = requests.Session()
session.auth = ('bgorham', 'Milorat22!')


with open('LV1074', 'a') as f:
    while True:
        response = session.get(locations)
        if response.status_code == 401:
            auth = session.post('http://10.221.247.237:8080/api')
        elif response.status_code == 200:
            rjson = response.json()
            machineLocations = rjson['machineLocations']
            for machine in machineLocations:
                if machine['name'] == "LV1074":
                    active = machine['active']
                    speed = machine['speed']['magnitude']
                    x = machine['xyz']['x']['magnitude']
                    y = machine['xyz']['y']['magnitude']
                    z = machine['xyz']['z']['magnitude']
                    heading = machine['heading']['magnitude']
                    timestamp = machine['timestamp']
                    gpsAccuracy = machine['gpsAccuracy']
                    heartbeatLost = machine['heartbeatLost']
                    shutdown = machine['shutdown']

                    line = '{},{},{},{},{},{},{},{},{},{},{}\n'.format('LV1074', timestamp, active, speed, x, y, z, heading, gpsAccuracy, heartbeatLost, shutdown)

                    f.write(line)
                    print(speed)
                    break
                
                

        time.sleep(1)