import cv2
import numpy as np
import Particles

def call_back(value):
    pass

cap = cv2.VideoCapture(0)
width = 600
height = 460
base = 10
a = Particles.star(width, height)
env = Particles.Environment(width, height)
env.addParticles(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,width);
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height);
while(1):

    # Take each frame
    _, frame1 = cap.read()
    frame = cv2.flip(frame1,1)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.createTrackbar("RED", "frame",100,255, call_back)
    cv2.createTrackbar("GREEN", "frame",100,255, call_back)
    cv2.createTrackbar("BLUE", "frame",100,255, call_back)
    
    # define range of blue color in HSV
    B = cv2.getTrackbarPos("BLUE", "frame")
    G = cv2.getTrackbarPos("GREEN", "frame")
    R = cv2.getTrackbarPos("RED", "frame")
    h = cv2.cvtColor(np.uint8([[[B, G, R]]]), cv2.COLOR_BGR2HSV)
    #bgr=np.array((int(bgr[0][0][0]),int(bgr[0][0][1]), int(bgr[0][0][2])))
    cv2.circle(frame, (20,20), 20, (B,G,R), -1)
    lower_blue = np.array([h[0][0][0]-10 ,100,100])
    upper_blue = np.array([h[0][0][0]+10,255,255])
    # lower_blue = np.array([h-10,100,100])
    # upper_blue = np.array([h+10,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
#     imgray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     ret,thresh = cv2.threshold(imgray,127,255,0)
#     contours= cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
#     frame = cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
 
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
 
        # only proceed if the radius meets a minimum size
        
        if radius > 20:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            a.refresh(base * round(x/base),base * round(y/base),radius)
            env.update()
            for p in env.particles:
                a.collide(p)
                cv2.circle(frame, (int(p.x), int(p.y)), int(p.size), p.color, -1)
            cv2.circle(frame, (int(a.x), int(a.y)), int(a.size),(0, 255, 255), -1)
    cv2.imshow('frame',frame)
    k = cv2.waitKey(5) & 0xFF
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()