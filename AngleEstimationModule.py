# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:09:02 2022

@author: Vignesh
"""
#Importing libraries
import cv2
import PoseEstimationModule as pm
import numpy as np

def main():
    #Reading the video
    video = cv2.VideoCapture('Pose Estimation/pose3.avi')
    
    #Creating an object for the class
    pEstimate = pm.poseEstimation()
    
    def successCheck(angle, side):
        global successLanding
        if side == 'rightBottom':
            successLanding = 0
            #Converting the angle to percentage
            per = np.interp(angle, (178, 120), (100, 0))
            #Checking for the perfect landing on Left Side
            if per == 100:
                print ('Check pass rightbottom')
                successLanding = 1
                return successLanding
            
        elif side == 'leftBottom':
            successLanding = 0
            #Converting the angle to percentage
            per = np.interp(angle, (175,240), (0, 100))
            #Checking for the perfect landing on Left Side
            if per == 100:
                print ('Check pass leftbottom')
                successLanding = 1
            return successLanding
           
        elif side == 'leftTop':
            successLanding = 0
            #Converting the angle to percentage
            per = np.interp(angle, (160,105), (100, 0))
            #Checking for the perfect landing on Left Side
            if per == 100:
                print ('Check pass lefttop')
                successLanding = 1
            return successLanding
            
        else:
            successLanding = 0
            #Converting the angle to percentage
            per = np.interp(angle, (260,250), (0, 100))
            #Checking for the perfect landing on Left Side
            if per == 100:
                print ('Check pass right top')
                successLanding = 1
            return successLanding
            
        
    def writeText(text, passFail = False, coordinate1 = (30,50), 
                  coordinate2 = (30,120)):
        if passFail == True:
            cv2.rectangle(frame, (0, 150), (1280, 0), (0, 0, 0), cv2.LINE_AA)
            cv2.putText(frame, str(text), coordinate1, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
            cv2.putText(frame, str('Pass'), coordinate2, 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 204, 102), 10)
        else:
            cv2.rectangle(frame, (0, 150), (1280, 0), (0, 0  , 0), cv2.LINE_AA)
            cv2.putText(frame, str(text), coordinate1, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
            cv2.putText(frame, str('Fail'), coordinate2, 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 10) 
    #Looping through each frame of the video
    while True:
        #Checking whether the frame has valid image and getting the current frame
        success, frame = video.read()
    
        #Resizing the video
        if frame is not None:
            frame = cv2.resize(frame, (1280, 720))
    
            #Detecting the coordinates
            frame = pEstimate.detectCoordinates(frame, False)
        
            #Fetching the Coordinates
            xyList = pEstimate.findCoordinates(frame, False)
        
            #Only if the coordinates are detected it will run
            if len(xyList) != 0:
                #Angle for Right Side Leg
                angleLeftBottom = pEstimate.toFindAngle(frame, 23, 25, 27, 
                                                        False)
                #Angle for Left Side Leg
                angleRightBottom = pEstimate.toFindAngle(frame, 24, 26, 28, 
                                                         False)
                #Angle for Right Side Body
                angleLeftTop = pEstimate.toFindAngle(frame, 11, 23, 25, False)
                #Angle for Left Side Body
                angleRightTop = pEstimate.toFindAngle(frame, 12, 24, 26, False)
                passCheckLeftBottom.append(successCheck(angleLeftBottom, 
                                                        'leftBottom'))
                passCheckRightBottom.append(successCheck(angleRightBottom, 
                                                         'rightBottom'))
                passCheckLeftTop.append(successCheck(angleLeftTop, 'leftTop'))
                passCheckRightTop.append(successCheck(angleRightTop, 
                                                      'rightTop'))
                
                finalCheck = ['leftBottom', 'rightBottom', 'leftTop', 'rightTop']
                for each in finalCheck:
                    if each == 'leftBottom':
                        if 1 in passCheckLeftBottom:
                            writeText('Left Bottom', True, (30,50), (30,120))
                        else:
                            writeText('Left Bottom', False, (30,50), (30,120))
                    elif each == 'rightBottom':
                        if 1 in passCheckRightBottom:
                            writeText('Right Bottom', True, (430,50), (430,120))
                        else:
                            writeText('Right Bottom', False, (430,50), (430,120))
                    elif each == 'leftTop':
                        if 1 in passCheckLeftTop:
                            writeText('Left Top', True, (730,50), (730,120))
                        else:
                            writeText('Left Top', False, (730,50), (730,120))
                    else:
                        if 1 in passCheckRightTop:
                            writeText('Right Top', True, (1100,50), (1100,120))
                        else:
                            writeText('Right Top', False, (1100,50), (1100,120))
            cv2.imshow("Pose Estimation", frame)    
        
            #Breaking the loop to close the window by pressing 'q' key
            #Masking the 28 bit of key pressed with the unique code
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
        # Close all the windows
        else:
            cv2.destroyAllWindows()
            break
        ##
        
# Main function    
if __name__ == "__main__":
    successLanding = 0
    passCheckLeftBottom = []
    passCheckRightBottom = []
    passCheckLeftTop = []
    passCheckRightTop = []
    main()
##