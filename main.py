import cv2
import math
import numpy as np

class Vision(object):
  def __init__(self):
    self.hslRange = {'hue': {'min': 80, 'max': 100}, 'sat': {'min': 60, 'max': 255}, 'lum': {'min': 0, 'max': 255}}
    self.focalLength = 980
    self.realCoordinates = np.array([
      (-5.125, 2.5, 0), # top left of left target
      (-3.125, 2.5, 0), # top right of left target
      (-5.125, -2.5, 0), # bottom left of left target
      (-3.125, -2.5, 0), # bottom right of left target
      (3.125, 2.5, 0), # top left of right target
      (5.125, 2.5, 0), # top right of right target
      (3.125, -2.5, 0), # bottom left of right target
      (5.125, -2.5, 0) # bottom right of right target
    ], dtype=np.float)

    self.cameraMatrix = np.array([
      (1.1604687468751836e+03, 0, 640),
      (0, 1.1604687468751836e+03, 426),
      (0, 0, 1)
    ], dtype=np.float)

    self.distortionMatrix = np.array([
      -1.3906801849944408e-01,
      1.8194213754829054e+00,
      0,
      0,
      -8.3069705607294129e+00
    ], dtype=np.float)

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

  def getCartesianFromContour(self, contour):
    moment = cv2.moments(contour)
    x = int(moment['m10'] / moment['m00'])
    y = int(moment['m01'] / moment['m00'])
    return {'x': x, 'y': y}

  def pixelToAngle(self, x, y, width, height):
    yaw = math.degrees(math.atan((x - ((width - 1) / 2) / self.focalLength)))
    pitch = math.degrees(math.atan((y - ((height - 1) / 2) / self.focalLength)))
    return {'yaw': yaw, 'pitch': pitch}

  def run(self, source):
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
    (rodRotation, jacobian) = cv2.Rodrigues(rotation)
    print(translation)
    print([np.dot(rodRotation, translation), np.dot(0, 1)])

    #cv2.imshow("Image", source)
    #cv2.waitKey(0)


visionTest = Vision()

visionTest.run(cv2.imread('sample.jpg'))
