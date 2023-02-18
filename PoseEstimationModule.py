# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 00:35:40 2022

@author: Vignesh
"""

#Importing libraries
import cv2
import mediapipe as mp
import time
import math


class poseEstimation():

    #Initialization Method
    def __init__(self, static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, 
                                     self.model_complexity,
                                     self.smooth_landmarks, 
                                     self.enable_segmentation,
                                     self.smooth_segmentation, 
                                     self.min_detection_confidence,
                                     self.min_tracking_confidence)
    ##
    
    def detectCoordinates(self, video, draw=True):

        # Converting the video from BGR to RGB to make it compatible for 
        # Mediapipe package
        videoRGB = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        ##

        #Pose detection by processing
        self.processed = self.pose.process(videoRGB)
        self.landmarks = self.processed.pose_landmarks

        #If pose joins are present then we have to draw the landmarks of the joins
        if self.landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    video, self.landmarks, self.mpPose.POSE_CONNECTIONS)

        return video

    def findCoordinates(self, video, draw=True):
        self.coordinates = []
        #If pose joins are present then we have to draw the landmarks of the joins
        if self.landmarks:
            for index, lm in enumerate(self.landmarks.landmark):
                height, width, channel = video.shape
                #To convert the ratio of the image (in decimal) to pixel value
                x, y = int(lm.x*width), int(lm.y*height)

                #Appending all the joints coordinates into an array
                self.coordinates.append([index, x, y])
                
                if draw:
                    cv2.circle(video, (x, y), 5, (255, 0, 0), cv2.FILLED)
        return self.coordinates
    
    def toFindAngle(self,frame,i1,i2,i3, draw = True):
        
        #To get the coordinates/landmarks of 3 points
        x1,y1 = self.coordinates[i1][1:]
        x2,y2 = self.coordinates[i2][1:]
        x3,y3 = self.coordinates[i3][1:]
        
        #Angle Calculation
        
        #Also needs to convert to degree from radian
        angle = math.degrees(math.atan2(y3-y2,x3-x2)- math.atan2(y1-y2,x1-x2))
        
        #Incase angle goes to negative then we must do some adjustment by adding 360 to it
        if angle <0:
            angle += 360   
        
        if draw:
            cv2.line(frame, (x1,y1),(x2,y2),(255,0,0),3)
            cv2.line(frame, (x3,y3),(x2,y2),(255,0,0),3)
            cv2.circle(frame, (x1,y1), 10, (255,0,0), cv2.FILLED)
            cv2.circle(frame, (x2,y2), 10, (255,0,0), cv2.FILLED)
            cv2.circle(frame, (x3,y3), 10, (255,0,0), cv2.FILLED)
            cv2.putText(frame, str(int(angle)),(x2-70,y2+20),
                        cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        return angle

#Main method for this file
def main():
    #Reading the video
    video = cv2.VideoCapture('Pose Estimation/pose2.avi')
    pTime = 0

    #Creating an object for the class
    pEstimate = poseEstimation()

    #Looping through each frame of the video
    while True:
        #Checking whether the frame has valid image and getting the current frame
        sucess, frame = video.read()
        
        #Resizing the video
        frame = cv2.resize(frame, (1100,820))

        #Calling the method for detecting the coordinates
        detector = pEstimate.detectCoordinates(frame)
        
        #Calling the method finding the coordinates
        coordinates = pEstimate.findCoordinates(detector, draw=False)
        
        if len(coordinates) != 0:
            cv2.circle(frame, (coordinates[11][1],coordinates[11][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[12][1],coordinates[12][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[23][1],coordinates[23][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[24][1],coordinates[24][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[25][1],coordinates[25][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[26][1],coordinates[26][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[27][1],coordinates[27][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, (coordinates[28][1],coordinates[28][2]), 8, 
                       (255, 0, 0), cv2.FILLED)
            
            
        #Checking the FPS
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        #Displaying the FPS in the video
        cv2.putText(frame, str(int(fps)), (70, 50),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        cv2.imshow("Pose Estimation", frame)
        
        
        #Breaking the loop to close the window by pressing 'q' key
        #Masking the 28 bit of key pressed with the unique code
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break


#When importing this file as Module this will be ignored else main() will be called
if __name__ == "__main__":
    main()
##