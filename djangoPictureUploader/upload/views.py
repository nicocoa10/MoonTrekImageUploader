import sys

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


def verify(request):

    return render(request, "upload/verify.html")

def upload(request):
    if request.method=="POST":
        form = CaptureForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()  # saves to database

            # EXIF CODE - need to add code to analyze the EXIF data
            img_file = form.cleaned_data['image']
            image = Image.open(img_file)
            exif = {}
            latitude = {}
            longitude = {}
            coordinates = {}

            img_exif = image.getexif()
            if img_exif:  # If image has exif

                # print(dict(img_exif))   #This prints the whole exif data

                for tag, value in image._getexif().items():
                    if tag in TAGS:
                        exif[TAGS[tag]] = value
                # Handle a photo with no GPS information (no coordinates)
                if 'GPSInfo' not in exif:
                    print('Your file does not have GPSInfo. Please upload a photo with the appropriate metadata.')
                    #If the image didnt gave GPS INFO we will send them to verify page to ask them for the gps info
                # Handle a photo with  GPS information ( Prints coordinates to console) and saves the image to db since its useful
                elif 'GPSInfo' in exif:
                    latitude = str(
                        float((exif['GPSInfo'][2][0]) + ((exif['GPSInfo'][2][1]) / 60) + ((exif['GPSInfo'][2][2]) / 3600)))

                    longitude = str(
                        float((exif['GPSInfo'][4][0]) + ((exif['GPSInfo'][4][1]) / 60) + ((exif['GPSInfo'][4][2]) / 3600)))

                    coordinates = (latitude + exif['GPSInfo'][1] + ", " + longitude + exif['GPSInfo'][3])

                    #Once you obtain the coordinates print it to console
                    print("Coordinates for file: " + str(img_file) + ": ")
                    print(coordinates)

                    # If the image had the GPS INFO we will still send them to a verify page just asking if the gotten location was correct
            else:
                print("Sorry, image has no exif data.")
                #If the image didnt have exif data we will send the users to verify ALL DATA of the image , pretty much like a form

            return verify(request)  # The goal is at the end to send the user to verify page, for verification regardless if image had gps location , or it had exif data.


    else:
        form = CaptureForm()

    my_form = {
        'form': form
    }
    return render(request, "upload/upload.html", context=my_form)


