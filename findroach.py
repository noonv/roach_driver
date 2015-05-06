#!/usr/bin/env python

'''
find roach on image

http://robocraft.ru

'''

import cv2
import sys

def nothing(*arg, **kw):
    pass
    
def find_roach(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blockSize = 109
    C = 53
    
    x1 = 55
    y1 = 16
    x2 = 258
    y2 = 219
    
    print("blockSize: {0} C: {1}".format(blockSize, C))
    bina = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blockSize, C)
    cv2.imshow('roacha', bina) 
    
    roi = bina[y1:y2, x1:x2]
    cv2.imshow('roach', roi)
    
    roi2 = img[y1:y2, x1:x2]
    
    contours, hierarchy = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Choose largest contour
    best = 0
    maxsize = 0
    count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > maxsize :
            maxsize = cv2.contourArea(cnt)
            best = count
        count = count + 1
    x,y,w,h = cv2.boundingRect(contours[best])
    cv2.rectangle(roi2, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.circle(roi2, (x+w/2, y+h/2), 2, (0, 255, 0), -1)
    
    cv2.imshow('roi2', roi2)

if __name__ == '__main__':
    print __doc__
    
    cv2.namedWindow('roacha')

    img = cv2.imread("screen-roach.png")
    
    find_roach(img)
    ch = cv2.waitKey(0)
    cv2.destroyAllWindows()
