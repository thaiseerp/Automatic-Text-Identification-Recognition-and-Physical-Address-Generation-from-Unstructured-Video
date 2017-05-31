import numpy as np
import cv2

imagec = cv2.imread('../Files/frames/2.jpg',0)
imagec = cv2.resize(imagec,(0,0),fx=0.5,fy=0.5)
image = cv2.imread('../Files/frames/2.jpg',1)
image = cv2.resize(image,(0,0),fx=0.5,fy=0.5)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255,
                       cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

'''
cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
print("[INFO] {} unique contours found".format(len(cnts)))

# loop over the contours
for (i, c) in enumerate(cnts):
    # draw the contour
    ((x, y), _) = cv2.minEnclosingCircle(c)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

hor_proj = []
ver_proj = []
for i in range(rows):
    hor_proj.append(sum(thres_img[i]))

'''

rows,cols = thresh.shape

ver_kernel = np.ones((11,11),np.uint8)
hor_kernel = np.ones((11,11),np.uint8)
ver_dilation = cv2.dilate(thresh,ver_kernel,iterations = 1)
hor_dilation = cv2.dilate(thresh,hor_kernel,iterations = 1)

image1 = [[0 for x in range(cols)] for y in range(rows)]
images = np.array(image1,np.uint8)
cv2.bitwise_and(ver_dilation, hor_dilation, images, mask=None)

'''

cnts = cv2.findContours(ver_dilation.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)[-2]
print("[INFO] {} unique contours found".format(len(cnts)))

# loop over the contours
for (i, c) in enumerate(cnts):
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

for (k, c) in enumerate(cnts):
    if cv2.contourArea(c)>20000:
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
'''

mask = np.zeros((rows+2, cols+2), np.uint8)
cv2.floodFill(ver_dilation, mask, (0,0), 255)
kernel = np.ones((50,50),np.uint8)
closing = cv2.morphologyEx(ver_dilation, cv2.MORPH_OPEN, kernel)

for j in range(cols):
    for i in range(rows):
        if closing[i,j] == 255:
            image[i,j] = 255,255,255




#cv2.imshow("Thresh", imagec)
cv2.imwrite("segmented.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
