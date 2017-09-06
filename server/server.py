#!/usr/bin/env python
import json
from flask import Flask, request, render_template, Response
import gevent.pywsgi
import gevent.monkey
gevent.monkey.patch_all()

from camera import Camera
from generateCalibration import GenerateCalibration

app = Flask(__name__)

cameraInstance = Camera()
runCalibration = GenerateCalibration('frames', '../calibration.json')

import time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hsl')
def hslPage():
    return render_template('hsl.html')

@app.route('/calibrate')
def calibratePage():
    return render_template('calibrate.html')

def genStream(camera, processed=False):
    while True:
        if (processed == True):
            frame = camera.getResultFrame()
        else:
            frame = camera.get_frame()
            
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.005) # yes, this delay is intentional.
                          # maybe it's a hack, but hey, it works.

@app.route('/stream')
def stream():
    return Response(genStream(cameraInstance), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/streamResult')
def streamResult():
    return Response(genStream(cameraInstance, processed=True), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/post', methods=['POST'])
def post():
    if (request.form['action'] == 'changeHSL'):
        cameraInstance.changeHSL({'component': request.form['component'], 'min': request.form['min'], 'max': request.form['max']})

    elif (request.form['action'] == 'getHSL'):
        return json.dumps(cameraInstance.getHSL())

    elif (request.form['action'] == 'saveHSL'):
        return str(cameraInstance.saveHSL())

    elif (request.form['action'] == 'setExposure'):
        return str(cameraInstance.setExposure(int(request.form['exposure'])))

    return str(True)

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
    gevent_server = gevent.pywsgi.WSGIServer(('', 5000), app)
    gevent_server.serve_forever()
