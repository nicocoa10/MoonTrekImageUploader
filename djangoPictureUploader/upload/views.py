from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
# Create your views here.
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

# upload view in Upload App created by Nicolas Ojeda
# This view recieves a request from the client with a picture
# in which can be accessed using FILES[] and specifying the name of the input which is declared in the html form
# this view gets the file and saves it . By default is saved in MEDIA_ROOT , specified in the settings.py of the project
# At the end it it returns to upload.html
# view is defined url is on the urls.py of this Upload App .
def upload(request):
    if request.method=="POST":
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        fs= FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
    return render(request,"upload/upload.html")
