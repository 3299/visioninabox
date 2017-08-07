import json
import cv2

import communications
import calculations

'''
Load configs
'''
with open('../config/calibration.json') as file:
  cameraMatrix = json.load(file)

with open('../config/hsl.json') as file:
     hsl = json.load(file)

with open('../config/coordinates.json') as file:
    coordinates = json.load(file)

# Init vision
vision = calculations.Vision(hsl['hsl'], coordinates['coordinates'], cameraMatrix)

# Init communications
udp = communications.Communicate(ip='127.0.0.1', port=1000)

while True:
    print(vision.run(cv2.imread('sample.jpg')))
