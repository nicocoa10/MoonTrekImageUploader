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

    for tag, value in image._getexif().items():
        if tag in TAGS:
            exif[TAGS[tag]] = value

    if 'DateTimeOriginal' not in exif:
        return("Image has no Date/Time information.")

    elif 'DateTimeOriginal' in exif:
        return(exif['DateTimeOriginal'])

# Create Address Finder here
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

def upload(request):
    if request.method=="POST":
        form = CaptureForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  # saves to database

            # EXIF CODE - need to add code to analyze the EXIF data
            img_file = form.cleaned_data['image']

            address = extractAddress(img_file)
            time = extractTime(img_file)

            return verify(request, address, time)  # The goal is at the end to send the user to verify page, for verification regardless if image had gps location , or it had exif data.


    else:
        form = CaptureForm()

    my_form = {
        'form': form
    }
    return render(request, "upload/upload.html", context=my_form)


def verify(request, coordinates, time):
    hasCoordinates = bool(coordinates)
    hasTime = bool(time)

    verify_dic = {
    'coordinates':coordinates,
    'hasCoordinates': hasCoordinates,
    'time' : time,
    'hasTime': hasTime,
    }

    return render(request, "upload/verify.html", context = verify_dic)


