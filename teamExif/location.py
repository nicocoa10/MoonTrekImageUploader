# import libraries 
from PIL import Image
from PIL.ExifTags import TAGS
# creat path for images
path = '/Users/elvira/Downloads/GettyVilla0001.JPG'
img_file = path
# open images
image =Image.open(img_file)
# creat dictionary
exif = {}
# convert tag value to tag name if it's in dictionary
for tag, value in image._getexif().items():
    if tag in TAGS:
        exif[TAGS[tag]]= value

# if image contain  GPSInfo tag we need to convert info to standart view 
if 'GPSInfo' in exif:
    geo_coordinate = '{0} {1} {2:.2f} {3},{4} {5} {6:.2f} {7}'. format(
        exif['GPSInfo'][2][0][0],
        exif['GPSInfo'][2][1][0],
        exif['GPSInfo'][2][2][0]/ exif['GPSInfo'][2][2][1],
        exif['GPSInfo'][1],
        exif['GPSInfo'][4][0][0],
        exif['GPSInfo'][4][1][0],
        exif['GPSInfo'][4][2][0]/ exif['GPSInfo'][2][2][1],
        exif['GPSInfo'][3]
    )
# print coordinate            
print(geo_coordinate)
print(exif['DateTimeDigitized'])
