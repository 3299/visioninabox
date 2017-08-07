#!/usr/bin/env python
import os
import sys
from flask import Flask, render_template, Response
import gevent.pywsgi
import gevent.monkey
gevent.monkey.patch_all()

sys.path.append('../shared')
from camera import Camera
from generateCalibration import GenerateCalibration

app = Flask(__name__)
cameraInstance = Camera()
runCalibration = GenerateCalibration('frames', '../calibration.json')

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(cameraInstance),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    # makes directory if it doesn't exist
    if not os.path.exists('frames'):
        os.makedirs('frames')

    # finds the highest int in filenames
    maxN = 0
    if (os.listdir('frames')):
        files = os.listdir('frames')
        for file in files:
            this = file.split('.')[0]
            if (this != ''):
                if (int(this) > maxN):
                    maxN = int(this)

    return str(cameraInstance.saveFrame('frames/' + str(maxN + 1) + '.jpg'))

@app.route('/calibrate')
def calibrate():
    return str(runCalibration.run())


if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    gevent_server = gevent.pywsgi.WSGIServer(('', 5000), app)
    gevent_server.serve_forever()
