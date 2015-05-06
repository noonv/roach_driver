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
    
    blockSize = cv2.getTrackbarPos('blockSize', 'roacha')
    C = cv2.getTrackbarPos('C', 'roacha')
    
    if blockSize % 2 == 0:
        blockSize = blockSize+1
    
    print("blockSize: {0} C: {1}".format(blockSize, C))
    bina = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blockSize, C)
    cv2.imshow('roacha', bina) 
    
    '''
    thrs = 90
    retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('roach', bin) 
    '''

if __name__ == '__main__':
    print __doc__
    
    cv2.namedWindow('roacha')
    cv2.createTrackbar('blockSize', 'roacha', 3, 200, nothing)
    cv2.createTrackbar('C', 'roacha', 0, 200, nothing)

    '''
    cv2.namedWindow('edge')
    cv2.createTrackbar('thrs1', 'edge', 2000, 5000, nothing)
    cv2.createTrackbar('thrs2', 'edge', 4000, 5000, nothing)
    '''

    img = cv2.imread("screen-roach.png")
    
    x1 = 55
    y1 = 16
    x2 = 258
    y2 = 219
    
    while True:
        find_roach(img)
        
        vis = img.copy()
        roi = vis[y1:y2, x1:x2]
        
        color = (0, 255, 0)
        cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2) 
        cv2.imshow('roi', vis)
        
        '''
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
        thrs2 = cv2.getTrackbarPos('thrs2', 'edge')
        edge = cv2.Canny(gray, thrs1, thrs2, apertureSize=5)
        vis = img.copy()
        vis /= 2
        vis[edge != 0] = (0, 255, 0)
        cv2.imshow('edge', vis)
        '''
        ch = cv2.waitKey(5)
        if ch == 27:
            break
    cv2.destroyAllWindows()
