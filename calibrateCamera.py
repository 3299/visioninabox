#!/usr/bin/env python
# Thank you to https://goo.gl/NDyw63

# Imports
import os
import json
import argparse
from glob import glob
import numpy as np
import cv2
from termcolor import colored

# CLI arguments
parser = argparse.ArgumentParser(description='Calculates the charateristics of a webcam from images of a calibration pattern.')
parser.add_argument('directory', metavar='directory', type=str,
                   help='the directory of images of the calibration pattern')
args = parser.parse_args()

if __name__ == '__main__':
    img_names = glob(os.path.abspath(args.directory) + '/*')
    square_size = 1.0

    pattern_size = (9, 6)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = 0, 0
    img_names_undistort = []
    for fn in img_names:
        print('processing %s... ' % fn, end='')
        img = cv2.imread(fn, 0)
        if img is None:
            print("Failed to load", fn)
            continue

        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size)
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)

        if not found:
            print('chessboard not found')
            continue

        img_points.append(corners.reshape(-1, 2))
        obj_points.append(pattern_points)

        print('ok')

    # calculate camera distortion
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)

    # Dump to JSON file
    with open('calibration.json', 'w') as f:
        json.dump({'matrix': camera_matrix.tolist(), 'distortion': dist_coefs.ravel().tolist(), 'rms': rms}, f, sort_keys = True, indent = 2)

    print(colored('Calculated and saved at calibration.json', 'green'))
