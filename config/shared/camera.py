import cv2
import json

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(16, -9)

        with open('../hsl.json') as file:
             self.hsl = json.load(file)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()

        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HLS),
          (float(self.hsl['h']['min']), float(self.hsl['s']['min']), float(self.hsl['l']['min'])),
          (float(self.hsl['h']['max']), float(self.hsl['s']['max']), float(self.hsl['l']['max'])))

        result = cv2.bitwise_and(frame, frame, mask=mask)

        # encode into JPG and return
        ret, jpeg = cv2.imencode('.jpg', result)
        return jpeg.tobytes()

    def saveFrame(self, filename):
        success, image = self.video.read()
        if (success == True):
            return cv2.imwrite(filename, image)
        else:
            return False

    def getHSL(self):
        with open('../hsl.json') as file:
             self.hsl = json.load(file)

        return self.hsl

    def changeHSL(self, hsl):
        if (hsl['component'] == 'h'):
            hsl.pop('component', 0)
            self.hsl['h'] = hsl
        elif (hsl['component'] == 's'):
            hsl.pop('component', 0)
            self.hsl['s'] = hsl
        elif (hsl['component'] == 'l'):
            hsl.pop('component', 0)
            self.hsl['l'] = hsl

    def saveHSL(self):
        with open('../hsl.json', 'w') as file:
            json.dump(self.hsl, file)
        return True
