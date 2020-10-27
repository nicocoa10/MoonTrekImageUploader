from django import forms
from .models import Capture
from django.template.defaultfilters import mark_safe


class CaptureForm(forms.ModelForm):
    class Meta:
        model = Capture
        fields= ('image',)


class ExifDataForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    city = forms.CharField(max_length=100 , label=mark_safe("<b> Enter City (Ex. Pomona)</b>"))
    state = forms.CharField(max_length=100,  label=mark_safe("<b> Enter state (Ex. California)</b>"))
    country = forms.CharField(max_length=100, label=mark_safe("<b>Enter City (Ex. US)</b>"))
    date = forms.DateField(help_text='Date (dd/mm/yyy)', label=mark_safe("<b>Date</b>"))
    time = forms.TimeField(help_text='Time (HH:MM) example 12:30',label=mark_safe("<b>Time</b>"))


    #All my attributes here