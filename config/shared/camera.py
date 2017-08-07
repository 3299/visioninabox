import cv2

class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.video.set(16, -9)

        self.hsl = {
            'h': {
                'min': 0,
                'max': 1
            },
            's': {
                'min': 0,
                'max': 1
            },
            'l': {
                'min': 0,
                'max': 1
            }
        }

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, frame = self.video.read()

        mask = cv2.inRange(cv2.cvtColor(frame, cv2.COLOR_BGR2HLS),
          (float(self.hsl['h']['min']) * 255, float(self.hsl['s']['min']) * 255, float(self.hsl['l']['min']) * 255),
          (float(self.hsl['h']['max']) * 255, float(self.hsl['s']['max']) * 255, float(self.hsl['l']['max']) * 255))

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
