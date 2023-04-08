# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:09:02 2022

@author: Vignesh
"""
# Importing libraries
import cv2
import PoseEstimationModule as pm
import numpy as np

def main(video, pEstimate, finalCheck, rotate = False):
    
    # Mainly used to check whether the landing and the bending of the player is
    # proper of not    
    def successCheck(angle, side):
        global successLanding
        
        # Specifically checking for the bending the body after successful 
        # landing
        
        # Right Side
        if side == 'rightBottom':
            successLanding = 0
            
            # Converting the angle to percentage
            percentage = np.interp(angle, (185, 295), (0, 100))
            ##
            
            # Returning the success/failure flag based on the percentage 
            # obtained before and after bending
            if percentage == 100:
                successLanding = 1
                return successLanding
            ##
        ##
        
        # Left Side
        else:
            successLanding = 0
            
            # Converting the angle to percentage
            percentage = np.interp(angle, (40,160), (100, 0))
            ##
            
            # Returning the success/failure flag based on the percentage 
            # obtained before and after bending
            if percentage == 100:
                successLanding = 1
            return successLanding
            ##
        ##
    ##
    
    # Using opencv library for creating a rectangle box and writing the text
    # for notifying whether the landing/bending is proper or improper    
    def writeText(text, passFail = False, coordinate1 = (30,50), 
                  coordinate2 = (30,120)):
        # For successful bending case
        if passFail == True:
            cv2.rectangle(frame, (0, 150), (1200, 0), (0, 0, 0), cv2.LINE_AA)
            cv2.putText(frame, str(text), coordinate1, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
            cv2.putText(frame, str('Pass'), coordinate2, 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 204, 102), 10)
        ##
        
        # For unsuccessful bending case
        else:
            cv2.rectangle(frame, (0, 150), (1200, 0), (0, 0  , 0), cv2.LINE_AA)
            cv2.putText(frame, str(text), coordinate1, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
            cv2.putText(frame, str('Fail'), coordinate2, 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 10) 
        ##
    ##
    
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
            frame = cv2.resize(frame, (1000, 820))
            ##
            
            # Rotating the video if required
            if rotate:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            ##
    
            # Detecting the coordinates of each frame and storing back as frame
            # for further estimation
            frame = pEstimate.detectCoordinates(frame, False)
            ##
        
            # Fetching each coordinates for each frame and storing it in 
            # an array, mainly this array helps us to check that in each frame
            # we determine the angle for the estimation
            xyList = pEstimate.findCoordinates(frame, False)
            ##
        
            # Looping through the array of coordination for the detected 
            # coordinates
            if len(xyList) != 0:
                
                # Estimating angle to verify whether it is successfull or not
                # Angle for Right Side Leg
                angleRightBottom = pEstimate.toFindAngleThreeCoordinates(frame, 24, 26, 28, 
                                                       False)
                ##
                angleLeftFoot = pEstimate.findAngleTwoCoordinates(frame, 29,31, True)
                angleRightFoot = pEstimate.findAngleTwoCoordinates(frame, 30,32, True)
                # Angle for Right Side Body
                angleRightTop = pEstimate.toFindAngleThreeCoordinates(frame, 12, 24, 26, False)
                ##
                ##
                
                # Arrays are used to store the pass/failure flag for obtaining
                # the results
                passCheckRightBottom.append(successCheck(angleRightBottom, 
                                                         'rightBottom'))
                passCheckRightTop.append(successCheck(angleRightTop, 
                                                      'rightTop'))
                ##
                
                # Finally for displaying the result in the video after checking
                # the final check flag on the both side
                for each in finalCheck:
                    # Checks if there is success flag in the array if yes,
                    # then the test is pass, else the test is failed
                    if each == 'rightBottom':
                        if 1 in passCheckRightBottom:
                            writeText('Right Bottom', True, (150,50), (150,120))
                        else:
                            writeText('Right Bottom', False, (150,50), (150,120))
                    else:
                        if 1 in passCheckRightTop:
                            writeText('Right Top', True, (530,50), (530,120))
                        else:
                            writeText('Right Top', False, (530,50), (530,120))
                    ##
                ##
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
        ##
        
# Main function    
if __name__ == "__main__":
    # Basic variables used for further estimation
    successLanding = 0
    passCheckLeftBottom = []
    passCheckRightBottom = []
    passCheckLeftTop = []
    passCheckRightTop = []
    finalCheck = ['rightBottom', 'rightTop']
    
    # Video as input for the initiating the estimation
    video = cv2.VideoCapture('Pose Estimation/pose2_r.avi')
    ##
    
    # Creating an object for the postestimation for reuse the logic of 
    # angle estimation, to fetch and detect the coordinates of each frame
    pEstimate = pm.poseEstimation()
    ##
    
    # Calling the main function
    main(video, pEstimate, finalCheck, True)
    ##
##