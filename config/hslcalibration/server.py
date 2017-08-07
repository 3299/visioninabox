#!/usr/bin/env python
import os
import sys
import json
from flask import Flask, request, render_template, Response
import gevent.pywsgi
import gevent.monkey
gevent.monkey.patch_all()

sys.path.append('../shared')
from camera import Camera

app = Flask(__name__)

cameraInstance = Camera()

import time

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.05) # yes, this delay is intentional.
                        # maybe it's a hack, but hey, it works.

@app.route('/video_feed')
def video_feed():
    return Response(gen(cameraInstance),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/streaming")
def streaming(request):
    def streaming_fn(response):
        while True:
            frame = cameraInstance.get_frame()
            response.write(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return response.stream(streaming_fn, content_type='multipart/x-mixed-replace; boundary=frame')

@app.route('/post', methods=['POST'])
def post():
    if (request.form['action'] == 'changeHSL'):
        cameraInstance.changeHSL({'component': request.form['component'], 'min': request.form['min'], 'max': request.form['max']})

    elif (request.form['action'] == 'getHSL'):
        return json.dumps(cameraInstance.getHSL())

    elif (request.form['action'] == 'saveHSL'):
        return str(cameraInstance.saveHSL())

    return str(True)

if __name__ == '__main__':
    gevent_server = gevent.pywsgi.WSGIServer(('', 5000), app)
    gevent_server.serve_forever()
