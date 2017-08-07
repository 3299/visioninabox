import cv2
import math
import numpy as np
import time

class Vision(object):
  def __init__(self, hslRange, coordinates, cameraMatrix):
    self.hslRange = hslRange
    self.focalLength = 980
    self.realCoordinates = np.array(coordinates, dtype=np.float)

    self.cameraMatrix = np.array(cameraMatrix['matrix'], dtype=np.float)

    self.distortionMatrix = np.array(cameraMatrix['distortion'], dtype=np.float)

  def getStrips(self, image):
    # Filter by HSL values
    thresholdImg = cv2.inRange(cv2.cvtColor(image, cv2.COLOR_BGR2HLS),
      (self.hslRange['hue']['min'], self.hslRange['sat']['min'], self.hslRange['lum']['min']),
      (self.hslRange['hue']['max'], self.hslRange['sat']['max'], self.hslRange['lum']['max']))

    # Get contours
    img, contours, hierarchy = cv2.findContours(thresholdImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Finds the 2 contours with the largest areas
    areaArray = []
    for contour in contours:
      areaArray.append({'area': cv2.contourArea(contour), 'contour': contour})

    areaArray.sort(key = lambda x: x['area'], reverse=True) # sorts by area in reverse order so that 2 largest will be first

    return [areaArray[0]['contour'], areaArray[1]['contour']]

  def getCorners(self, contour):
    left = tuple(contour[contour[:, :, 0].argmin()][0])
    right = tuple(contour[contour[:, :, 0].argmax()][0])
    top = tuple(contour[contour[:, :, 1].argmin()][0])
    bottom = tuple(contour[contour[:, :, 1].argmax()][0])

    return {'topLeft': (left[0], top[1]),
            'topRight': (right[0], top[1]),
            'bottomLeft': (left[0], bottom[1]),
            'bottomRight': (right[0], bottom[1]) }

  def run(self, source):
    # start FPS timer
    fpsStart = time.time()

    # Get size of source
    height = np.size(source, 0)
    width = np.size(source, 1)

    cornerPoints = []

    for strip in self.getStrips(source):
      corners = self.getCorners(strip)
      cv2.circle(source, corners['topLeft'], 4, (0, 0, 255), -1)
      cv2.circle(source, corners['topRight'], 4, (0, 255, 0), -1)
      cv2.circle(source, corners['bottomLeft'], 4, (255, 0, 0), -1)
      cv2.circle(source, corners['bottomRight'], 4, (255, 255, 0), -1)

      cornerPoints.append((corners['topLeft'][0], corners['topLeft'][1]))
      cornerPoints.append((corners['topRight'][0], corners['topRight'][1]))
      cornerPoints.append((corners['bottomLeft'][0], corners['topLeft'][1]))
      cornerPoints.append((corners['bottomRight'][0], corners['topRight'][1]))

    # show the output image
    # solve PnP problem
    (result, rotation, translation) = cv2.solvePnP(self.realCoordinates, np.array(cornerPoints, dtype=np.float), self.cameraMatrix, self.distortionMatrix)


    ZYX,jac=cv2.Rodrigues(rotation)

    totalrotmax=np.array([[ZYX[0,0],ZYX[0,1],ZYX[0,2],translation[0]],
    [ZYX[1,0],ZYX[1,1],ZYX[1,2],translation[1]],
    [ZYX[2,0],ZYX[2,1],ZYX[2,2],translation[2]],
    [0,0,0,1]])

    WtoC=np.mat(totalrotmax)

    inverserotmax=np.linalg.inv(totalrotmax)
    f=inverserotmax
    fps = 1 / (time.time() - fpsStart)
    return {'matrix': inverserotmax, 'FPS': fps}
