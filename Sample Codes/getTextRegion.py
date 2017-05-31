import numpy as np
import cv2

imged = cv2.imread('../Files/frames/2.jpg')
imged = cv2.resize(imged,(0,0),fx=0.5,fy=0.5)
img = cv2.imread('../Files/frames/2.jpg',0)
img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)

horizontal_kernel = np.array([[-1,-1,-1],[2,2,2],[-1,-1,-1]])
vertical_kernel = np.array([[-1,2,-1],[-1,2,-1],[-1,2,-1]])

hor_img = cv2.filter2D(img,-1,horizontal_kernel)
ver_img = cv2.filter2D(img,-1,vertical_kernel)

#cv2.imshow('Vertical Gradient Image',ver_img)
#cv2.imwrite('../Files/frames/initial/VerticalGradientImage.png',ver_img)
#cv2.imwrite('../Files/frames/initial/HorizontalGradientImage.png',hor_img)
#cv2.imshow('Horizontal Gradient Image',hor_img)

ret1,ver_thres_img = cv2.threshold(ver_img,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret2,hor_thres_img = cv2.threshold(hor_img,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

rows,cols = ver_thres_img.shape

#cv2.imshow('Vertical Threshold Image',ver_thres_img)
#cv2.imshow('Horizontal Threshold Image',hor_thres_img)
#cv2.imwrite('../Files/frames/initial/VerticalThresholdImage.png',ver_thres_img)
#cv2.imwrite('../Files/frames/initial/HorizontalThresholdImage.png',hor_thres_img)

ver_kernel = np.ones((8,8),np.uint8)
hor_kernel = np.ones((5,5),np.uint8)

ver_dilation = cv2.dilate(ver_thres_img,ver_kernel,iterations = 1)
hor_dilation = cv2.dilate(hor_thres_img,hor_kernel,iterations = 1)

#cv2.imshow('Vertical Dilated Image',ver_dilation)
#cv2.imshow('Horizontal Dilated Image',hor_dilation)
#cv2.imwrite('../Files/frames/initial/VerticalDilatedImage.png',ver_dilation)
#cv2.imwrite('../Files/frames/initial/HorizontalDilatedImage.png',hor_dilation)

image = [[0 for x in range(cols)] for y in range(rows)]
'''
for i in range(0,rows):
    for j in range(0,cols):
        if (ver_dilation[i,j] and hor_dilation[i,j])==255:
            #print(i,j)
            image[i][j] = 255
'''

image = np.array(image,np.uint8)
cv2.bitwise_and(ver_dilation, hor_dilation, image, mask=None)

#cv2.imshow('Bitwise and of both dilated image',image)
#cv2.imwrite('../Files/frames/initial/BitwiseAndImage.png',image)

kernel = np.ones((1,11),np.uint8)
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
new_kernel = np.ones((7,3),np.uint8)
abc = cv2.dilate(opening,new_kernel,iterations = 1)
final = cv2.addWeighted(img,0.7,abc,0.4,0)

cv2.imshow('Final',final)
#cv2.imwrite('../Files/frames/initial/final.png',final)
'''
image1 = image.copy()
(_,cnts, _) = cv2.findContours(image1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
screenCnt = None


# loop over our contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.1* peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

print(screenCnt)

cv2.drawContours(imged, [screenCnt], -1, (0, 255, 0), 3)
cv2.imshow("Coutour with four point", imged)
'''

cv2.waitKey(0)
cv2.destroyAllWindows()
