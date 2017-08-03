import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def getFrame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def saveFrame(self, filename):
        success, image = self.video.read()
        if (success == True):
            return cv2.imwrite(filename, image)
        else:
            return False


from flask import Flask, render_template, Response
import gevent.pywsgi
import gevent.monkey
gevent.monkey.patch_all()

import os

app = Flask(__name__)

camera = VideoCamera()

@app.route('/')
def index():
    return render_template('index.html')

def gen():
    while True:
        frame = camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/camerastream')
def video_feed():
    yield('')
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def saveImage():
    if not os.path.exists('calibrationImages'):
        os.makedirs('calibrationImages')

    if (os.listdir('calibrationImages')):
        lastImage = os.listdir('calibrationImages')[-1]
        lastImage = int(lastImage[:-4])
    else:
        lastImage = 0

    return str(camera.saveFrame('calibrationImages/' + str(lastImage + 1) + '.jpg'))

if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    gevent_server = gevent.pywsgi.WSGIServer(('', 5000), app)
    gevent_server.serve_forever()  # instead of flask_app.run()
