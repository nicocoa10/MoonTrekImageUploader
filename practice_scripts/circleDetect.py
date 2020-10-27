import numpy as np
import cv2 as cv
img = cv.imread ('001.jpg')
output = img.copy()
#Half circle transform to detect circles

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray,5)
circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT , 1, 20,param1=50, param2=30, minRadius=0, maxRadius=0) #will give the circle vector
detected_circles = np.uint16(np.around(circles))
print(circles)
# detected_circles = np.around(circles)

cv.Ho
# Draw detected circles in copy of image
rad=0

for (x,y,r) in detected_circles[0,:] :
    if r<350 and r>200:
        cv.circle(output,(x,y),r,(0,255,0),3)
    # cv.circle(output,(x,y),2,(0,255,255),3)


cv.imshow('output', output)
cv.waitKey(0)
cv.destroyAllWindows()

