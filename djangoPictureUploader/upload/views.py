import sys
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.generic import TemplateView
from .forms import CaptureForm
from geopy import Nominatim
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import requests


class Home(TemplateView):
    template_name = 'home.html'

# upload view in Upload App
# This view recieves a request from the client with a picture
# in which can be accessed using FILES[] and specifying the name of the input which is declared in the html form
# this view gets the file and saves it . By default is saved in MEDIA_ROOT , specified in the settings.py of the project
# At the end it it returns to upload.html
# view is defined url is on the urls.py of this Upload App .

# Make time function here
def extractTime(img_file):
    image = Image.open(img_file)
    exif = {}
    img_exif = image.getexif()
    if img_exif:  # If image has exif
        for tag, value in image._getexif().items():
            if tag in TAGS:
                exif[TAGS[tag]] = value

        if 'DateTimeOriginal' not in exif:
            return("Image has no Date/Time information.")

        elif 'DateTimeOriginal' in exif:
            return(exif['DateTimeOriginal'])
    else:
        print("Sorry, image has no exif data.")
        # return ("Image has no Date/Time information.")


# Create Address Finder here
def extractAddress(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}

    img_exif = image.getexif()
    if img_exif:  # If image has exif
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
    else:
        print("Sorry, image has no exif data.")
    geolocation = Nominatim(user_agent='test/1')
    # location = geolocation.reverse(coordinates)
    return(coordinates)

# Latitude Finder here
def extractLatitude(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}
    img_exif = image.getexif()
    if img_exif:  # If image has exif
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
    return coordinates

# Longitude Finder here
def extractLongitude(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}
    img_exif = image.getexif()
    if img_exif:
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
    return coordinates

# Create Coordinates Finder here
def extractCoordinates(img_file):
    image = Image.open(img_file)
    exif = {}
    latitude = {}
    longitude = {}
    coordinates = {}
    img_exif = image.getexif()
    if img_exif:
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

    return(coordinates)

def upload(request):
    if request.method=="POST":
        form = CaptureForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  # saves to database

            # EXIF CODE - need to add code to analyze the EXIF data
            img_file = form.cleaned_data['image']

            # address = extractAddress(img_file)
            time = extractTime(img_file)
            coordinates = extractCoordinates(img_file)
            lon = extractLongitude(img_file)
            lat = extractLatitude(img_file)

            #If there is coordinates data and time
            if (bool(coordinates) and bool(time)):
                return chooseCall(request,lon,lat,time)
            #If there is missing data
            else:
                return verify(request, lon, lat, time, coordinates)  # The goal is at the end to send the user to verify page, for verification regardless if image had gps location , or it had exif data.


    else:
        form = CaptureForm()

    my_form = {
        'form': form
    }
    return render(request, "upload/upload.html", context=my_form)

def chooseCall(request,lon,lat,time):

    chooseCall_dic = {
        'lon': lon,
        'lat': lat,
        'time': time,

    }

    return render(request, "upload/choose_call.html", context=chooseCall_dic)


def verify(request, lon, lat, time, coordinates):
    # If you want to add in the address, add "address" as a parameter of verify
    # hasAddress = bool(address)
    hasTime = bool(time)
    hasCoordinates = bool(coordinates)
    hasLon = bool(lon)
    hasLat = bool(lat)

    verify_dic = {
    'lon':lon,
    'hasLon':hasLon,
    'lat':lat,
    'hasLat':hasLat,
    'time' : time,
    'hasTime': hasTime,
    'coordinates': coordinates,
    'hasCoordinates': hasCoordinates,
    # 'hasAddress': address,
    }

    return render(request, "upload/verify.html", context = verify_dic)

def planetVectorAPICall(request,time):


    #time needs to be converted into the correct format, like below
    # time = '2019-10-07T01:10:45'

    #making a get request to Moon Trek Portal for planet vector search where origin is earth

    r = requests.get('http://54.157.167.17:5000/planet-vector-search/moon/earth/'+ timeConvertUTC(time))
    print(r.text) #should print the retrieved data to console

    json_object = r.json()
    # print(json_object['positions']['earth'])

    #saving the obtained data in a dictionary
    vector_dic=json_object['positions']['earth']

    #testing to console
    print(vector_dic['x'])
    print(vector_dic['y'])
    print(vector_dic['z'])


    return render(request, "upload/vector.html", context=vector_dic)

def nearestPointAPICall(request,lon,lat,time):

    #At this point lon and lat are recieved in the correct format
    #time needs to be converted into the correct format, like below
    # time = '2019-10-07T01:10:45'


    #making a get request to Moon Trek Portal for planet vector search where origin is earth
    r = requests.get('http://54.157.167.17:5000/nearest-point/earth/moon/' + lon+ '/' + lat+'/'+ timeConvertUTC(time))

    json_object = r.json()
    # print(type(json_object)) #just to test and print the contents of r to console , which should be the retrieved data

    #saving the obtained data in a dictionary
    nearestPoint_dic=json_object

    return render(request, "upload/nearest_point.html", context=nearestPoint_dic)


def timeConvertUTC(time):

    time_utc= '2019-10-07T01:10:45'
    return str(time_utc)
