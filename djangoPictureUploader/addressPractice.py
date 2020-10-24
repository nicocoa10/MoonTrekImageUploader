import os
import sys

# Must have geopy and pillow installed, built on python3

from geopy import Nominatim 
from PIL import Image
from PIL.ExifTags import TAGS

# Does not support HEIC
# If HEIC is changed to JPG, file is supported but EXIF data is VERY small
# Change an iPhone's settings from HEIC to Most Compatible to get EXIF data
# Tested and worked with photos taken directly with iPhone 11 and sent to laptop
# Screenshots, downloads, text message downloads will strip EXIF data

# img_file = 'moon1.jpg'

# Latitude Finder here
def extractLatitude(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}

    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value

    if 'GPSInfo' not in exif:
        print('Your file does not have GPSInfo. Please upload a photo with the appropriate metadata.')
        # Instead of exiting out, can work to ask user for different file name instead

    if 'GPSInfo' in exif:
        latitude = str(
            float((exif['GPSInfo'][2][0]) + ((exif['GPSInfo'][2][1]) / 60) + ((exif['GPSInfo'][2][2]) / 3600)))


        coordinates = (latitude + exif['GPSInfo'][1])
    #     N should be a positive coordinate, S should be a negative coordinate

    if 'N' or 'S' in coordinates:
        if 'N' in coordinates:
            coord = coordinates.replace("N", "")
        if 'S' in coordinates:
            strippedCoordinate = coordinates.replace("S","")
            coord = float(strippedCoordinate) * (-1)

    return(str(coord))

# Longitude Finder here
def extractLongitude(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}

    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value

    if 'GPSInfo' not in exif:
        print('Your file does not have GPSInfo. Please upload a photo with the appropriate metadata.')
        # Instead of exiting out, can work to ask user for different file name instead

    if 'GPSInfo' in exif:
        longitude = str(
            float((exif['GPSInfo'][4][0]) + ((exif['GPSInfo'][4][1]) / 60) + ((exif['GPSInfo'][4][2]) / 3600)))

        coordinates = (longitude + exif['GPSInfo'][3])
    #     W should be a negative coordinate, E should be a positive coordinate
    if 'W' or 'E' in coordinates:
        if 'E' in coordinates:
            coord = coordinates.replace("E", "")
        if 'W' in coordinates:
            strippedCoordinate = coordinates.replace("W","")
            coord = float(strippedCoordinate) * (-1)

    return(str(coord))

#Show tags
def showTags(img_file):
    image = Image.open(img_file)
    exif = {}

    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value
            print(str(TAGS[tag]) + ": " + str(value))

# showTags('iphonePic.JPG')

# Time function
def extractTime(img_file):
    image = Image.open(img_file)
    exif = {}

    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value

    if 'DateTimeOriginal' not in exif:
        return("Image has no Date/Time information.")

    elif 'DateTimeOriginal' in exif:
        return(exif['DateTimeOriginal'])


# Specific Address Finder
def extractAddress(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}

    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value

    if 'GPSInfo' not in exif:
        print('Your file does not have GPSInfo. Please upload a photo with the appropriate metadata.')
        # Instead of exiting out, can work to ask user for different file name instead

    if 'GPSInfo' in exif:
        latitude = str(
            float((exif['GPSInfo'][2][0]) + ((exif['GPSInfo'][2][1]) / 60) + ((exif['GPSInfo'][2][2]) / 3600)))

        longitude = str(
            float((exif['GPSInfo'][4][0]) + ((exif['GPSInfo'][4][1]) / 60) + ((exif['GPSInfo'][4][2]) / 3600)))

        coordinates = (latitude + exif['GPSInfo'][1] + ", " + longitude + exif['GPSInfo'][3])

    geolocation = Nominatim(user_agent='test/1')
    location = geolocation.reverse(coordinates)
    return(location.address)

latitude = extractLatitude('iphonePic.JPG')
longitude = extractLongitude('iphonePic.JPG')

print(latitude + ", " + longitude)
