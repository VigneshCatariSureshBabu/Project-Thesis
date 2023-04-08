# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:09:02 2022

@author: Vignesh
"""
# Importing libraries
import cv2

#import PoseEstimationModule as pm

class RightSideViewEstimation:
    
    def angleDisplay(frame,text, angle):
       cv2.rectangle(frame, (0, 150), (1280, 0), (0, 0, 0), cv2.LINE_AA)
       cv2.putText(frame, str(text), (30,50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
       
       cv2.putText(frame, str(angle), (30,120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 10)
      
   
   ##
    
    def mainEstimation(self,video, pEstimate,rotate = False):
        rsv = RightSideViewEstimation()
        # Looping through each frame of the video
        while True:
            # Checking whether the frame has valid image and getting 
            # the current frame
            success, frame = video.read()
        
            # Main checkpoint to verify whether the frame obtained is not none
            # mainly to avoid the assertion error while in the end of the video
            # if no frame is left the window opened are closed
            if frame is not None:
                
                # Resizing the video
                frame = cv2.resize(frame, (900, 820))
                ##
                
                # Rotating the video if required
                if rotate:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                ##
        
                # Detecting the coordinates of each frame and storing back as frame
                # for further estimation
                detector = pEstimate.detectCoordinates(frame, False)
                ##
            
                # Fetching each coordinates for each frame and storing it in 
                # an array, mainly this array helps us to check that in each frame
                # we determine the angle for the estimation
                xyList = pEstimate.findCoordinates(detector, False)
                ##
            
                # Looping through the array of coordination for the detected 
                # coordinates
                if len(xyList) != 0:
                    
                    # Angle for Right Side Ankle
                    angleRightAnkle = pEstimate.findAngleTwoCoordinates(frame, 30,32, True)
                    absAngleRightAnkle = abs(round(angleRightAnkle - 90))
                    print(absAngleRightAnkle)
                    rsv.angleDisplay("Ankle Plantar flexion: Right", absAngleRightAnkle)
                ##
                
                # Display the result text in each frame
                cv2.imshow("Pose Estimation", frame)    
                ##
                
                # Breaking the loop to close the window by pressing 'q' key
                # Masking the 28 bit of key pressed with the unique code
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
                ##
            ##    
            # Close all the windows
            else:
                cv2.destroyAllWindows()
                break
            #
