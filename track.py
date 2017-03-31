import cv2
import numpy as np
import Particles


cap = cv2.VideoCapture(0)
width = 600
height = 460
a = Particles.star(width, height)
env = Particles.Environment(width, height)
env.addParticles(2)
cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,width);
cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,height);
while(1):

    # Take each frame
    _, frame1 = cap.read()
    frame = cv2.flip(frame1,1)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

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
            a.refresh(x,y,radius)
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