#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image
from PIL.ExifTags import TAGS
from GPSPhoto import gpsphoto
import requests
from io import BytesIO
import pandas as pd
import json
import os
import sys
import pickle
from flask import Flask, request, jsonify, abort

app = Flask(__name__)
app.config["DEBUG"] = True

if not os.path.exists("database.pickle"):
    with open('database.pickle', 'wb') as handle:
        pickle.dump([], handle, protocol=pickle.HIGHEST_PROTOCOL)

def get_info(url):

    image = Image.open(url)
    
    exif ={}
    latitude = {}
    longitude = {}
    coordinates = {}
    
    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value
    
    if 'GPSInfo' not in exif:
     print('Your file does not have GPSInfo. Please upload a photo with the appropriate metadata.')
     sys.exit()
    
    if 'GPSInfo' in exif:
        latitude = str(float((exif['GPSInfo'][2][0]) + ((exif['GPSInfo'][2][1])/ 60) + ((exif['GPSInfo'][2][2])/3600)))
    
        longitude = str(float((exif['GPSInfo'][4][0]) + ((exif['GPSInfo'][4][1])/ 60) + ((exif['GPSInfo'][4][2])/3600)))
        
        coordinates = (latitude + exif['GPSInfo'][1] + ", " + longitude + exif['GPSInfo'][3])
    
    data = dict(url=url,
                coordinates=coordinates,
                datetime=exif['DateTimeDigitized'])

    file_path = 'database.pickle'
    file = open(file_path, 'rb')
    old_data = pickle.load(file)
    old_data.append(data)
    
    with open("database.pickle", "wb") as f:
        pickle.dump(old_data, f)
        
    return data

@app.route('/', methods=['GET', 'POST'])
def process_file():
    req_param = request.json
    url = req_param['image_url']
    exif_data = get_info(url)
    return jsonify(exif_data)

print('api ready')
if __name__ == '__main__':

    app.run(debug=False, host='127.0.0.1', port = 8055)










