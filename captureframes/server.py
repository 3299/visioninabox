#!/usr/bin/env python
import os
from flask import Flask, render_template, Response
import gevent.pywsgi
import gevent.monkey
gevent.monkey.patch_all()

from camera import Camera

app = Flask(__name__)
cameraInstance = Camera()

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
    if not os.path.exists('calibrationImages'):
        os.makedirs('calibrationImages')

    # finds the highest int in filenames
    maxN = 0
    if (os.listdir('calibrationImages')):
        files = os.listdir('calibrationImages')
        for file in files:
            this = file.split('.')[0]
            if (this != ''):
                if (int(this) > maxN):
                    maxN = int(this)

    return str(cameraInstance.saveFrame('calibrationImages/' + str(maxN + 1) + '.jpg'))


if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True)
    gevent_server = gevent.pywsgi.WSGIServer(('', 5000), app)
    gevent_server.serve_forever()
