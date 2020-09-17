import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
# Does not support HEIC
# If HEIC is changed to JPG, file is supported but EXIF data is VERY small
# Change an iPhone's settings from HEIC to Most Compatible to get EXIF data

# Copy and paste the printed results from 'print(coordinates)' into google to get a location.
# Next step is finding how to get the address from the coordinates 
img_file = '4thJuly.JPG'
image = Image.open(img_file)

exif ={}
latitude = {}
longitude = {}
coordinates = {}

for tag, value in image._getexif().items():
    if tag in TAGS:
        exif[TAGS[tag]] = value
# Handle a photo with no GPS information (no coordinates)
if 'GPSInfo' not in exif:
 print('Your file does not have GPSInfo. Please upload a photo with the appropriate metadata.')
 sys.exit()

if 'GPSInfo' in exif:
    latitude = str(float((exif['GPSInfo'][2][0]) + ((exif['GPSInfo'][2][1])/ 60) + ((exif['GPSInfo'][2][2])/3600)))

    longitude = str(float((exif['GPSInfo'][4][0]) + ((exif['GPSInfo'][4][1])/ 60) + ((exif['GPSInfo'][4][2])/3600)))
    
    coordinates = (latitude + exif['GPSInfo'][1] + ", " + longitude + exif['GPSInfo'][3])

print(coordinates)
