#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import requests 

# defining the api-endpoint  
API_ENDPOINT = "http://127.0.0.1:8055/"

# path to the image or video
image_url = '/Users/tony/Downloads/IMG_0246 (1).JPG'

# data to be sent to api 
data = {'image_url':image_url} 

# sending post request and saving response as response object 
r = requests.get(url = API_ENDPOINT, json = data) 
  
# extracting response text  
exif_data = r.json()
