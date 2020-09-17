from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.generic import TemplateView

from .forms import CaptureForm

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
            form.save()

    else:
        form = CaptureForm()

    my_form = {
        'form': form
    }
    return render(request, "upload/upload.html", context=my_form)


