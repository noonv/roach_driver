#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
find and follow by roach

For usage:
sudo apt-get install libopencv-dev python-opencv
sudo modprobe bcm2835-v4l2

http://robocraft.ru
'''

import cv2
import sys
import serial
SERIAL_PORT = '/dev/ttyUSB0' #'COM1'
SERIAL_SPEED = 57600

    
def find_roach(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    blockSize = 109
    C = 53
    
    x1 = 55
    y1 = 16
    x2 = 258
    y2 = 219
    
    #print("blockSize: {0} C: {1}".format(blockSize, C))
    bina = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, blockSize, C)
    #cv2.imshow('roacha', bina) 
    
    roi = bina[y1:y2, x1:x2]
    #cv2.imshow('roach', roi)
    #cv2.imwrite("roach.png", roi)
    
    #roi2 = img[y1:y2, x1:x2]
    
    contours, hierarchy = cv2.findContours(roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    center_x = -1
    center_y = -1
    
    if len(contours) > 0:
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
        center_x = x+w/2
        center_y = y+h/2
        
        #cv2.rectangle(roi2, (x,y), (x+w,y+h), (0,255,0), 2)
        #cv2.circle(roi2, (center_x, center_y), 2, (0, 255, 0), -1)
    
    #cv2.imshow('roi2', roi2)
    
    return (center_x, center_y)

if __name__ == '__main__':
    print __doc__
    
    try:
        ser = serial.Serial(SERIAL_PORT, SERIAL_SPEED)
    except Exception as detail:
        print("ERROR: Open Serial!")
        print(detail)
        sys.exit(1)
    
    try:
        cap = cv2.VideoCapture(0)
    except Exception as detail:
        print("ERROR: Camera initialization failed!")
        print(detail)
        sys.exit(1)
        
    cap.set(3, 320)
    cap.set(4, 240)
    #img = cv2.imread("screen-roach.png")
    
    prev_x = -1
    prev_y = -1
    
    while True:
        ret, frame = cap.read()
        #cv2.imwrite("frame.png", frame)
        x,y = find_roach(frame)
        print("x: {0} y: {1}".format(x, y))
        if x != -1 and y != -1:
            if prev_x == -1 and prev_y == -1:
                prev_x = x
                prev_y = y
            if abs(prev_x - x) > 2 or abs(prev_y - y) > 2 :
                if x > prev_x :
                    print("left")
                    ser.write("a")
                elif prev_x > x :
                    print("right")
                    ser.write("d")
                if y > prev_y :
                    print("back")
                    ser.write("s")
                elif prev_y > y:
                    print("forward")
                    ser.write("w")
            else:
                print("stop")
                ser.write(" ")
            prev_x = x
            prev_y = y
        
        ch = cv2.waitKey(150)
        if ch == 27:
            break
            
    ser.close()
    cap.release()
    #cv2.destroyAllWindows() 
