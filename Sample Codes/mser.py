import cv2
import numpy as np


def countingsort( aList, k ):
    counter = [0] * ( k + 1 )
    for i in aList:
      counter[i] += 1

    ndx = 0;
    for i in range( len( counter ) ):
      while 0 < counter[i]:
        aList[ndx] = i
        ndx += 1
        counter[i] -= 1
    return aList

img = cv2.imread('../Files/frames/3.jpg')
img = cv2.resize(img,(0,0),fx=0.5,fy=0.5)


mser = cv2.MSER_create()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
vis = img.copy()

regions, _ = mser.detectRegions(gray)

hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
cv2.polylines(vis, hulls, 1, (0, 255, 0))

cv2.imshow('img', vis)
cv2.waitKey(0)
cv2.destroyAllWindows()