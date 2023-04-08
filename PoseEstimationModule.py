# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 00:35:40 2022

@author: Vignesh
"""

#Importing libraries
import cv2
import mediapipe as mp
import math
##

class poseEstimation():

    # Initialization Method
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
    
    # Detecting the coordinates of each frame and storing back as frame
    # for further estimation
    def detectCoordinates(self, video, draw=True):

        # Converting the video from BGR to RGB to make it compatible for 
        # Mediapipe package
        videoRGB = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        ##

        # Pose detection by processing
        self.processed = self.pose.process(videoRGB)
        self.landmarks = self.processed.pose_landmarks
        ##
        
        # If pose joins are present then we have to draw the landmarks of 
        # the joins
        if self.landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    video, self.landmarks, self.mpPose.POSE_CONNECTIONS)

        return video
        ##
    ##
    
    # Fetching each coordinates for each frame and storing it in 
    # an array, mainly this array helps us to check that in each frame
    # we determine the angle for the estimation
    def findCoordinates(self, video, draw=True):
        self.coordinates = []
        
        # If pose joins are present then we have to draw the landmarks of 
        # the joins
        if self.landmarks:
            for index, lm in enumerate(self.landmarks.landmark):
                height, width, channel = video.shape
                # To convert the ratio of the image (in decimal) to pixel value
                x, y = int(lm.x*width), int(lm.y*height)
                ##

                # Appending all the joints coordinates into an array
                self.coordinates.append([index, x, y])
                ##
                
                # To mark the coordinates into the frame
                if draw:
                    cv2.circle(video, (x, y), 5, (255, 0, 0), cv2.FILLED)
                ##
        return self.coordinates
        ##
    ##
    
    # Determining the angle for the future verification whether it is 
    # successfull or not
    def toFindAngleThreeCoordinates(self,frame,i1,i2,i3, draw = True):
        
        # To get the coordinates/landmarks of 3 points
        x1,y1 = self.coordinates[i1][1:]
        x2,y2 = self.coordinates[i2][1:]
        x3,y3 = self.coordinates[i3][1:]
        ##
        
        # Angle Calculation
        # Also needs to convert to degree from radian
        angle = math.degrees(math.atan2(y3-y2,x3-x2)- math.atan2(y1-y2,x1-x2))
        ##
        
        # Incase angle goes to negative then we must do some adjustment by 
        # adding 360 to it
        if angle <0:
            angle += 360 
        ##
        
        # Connect all the landmarks with the coordinates into each frame
        if draw:
            cv2.line(frame, (x1,y1),(x2,y2),(255,0,0),3)
            cv2.line(frame, (x3,y3),(x2,y2),(255,0,0),3)
            cv2.circle(frame, (x1,y1), 10, (255,0,0), cv2.FILLED)
            cv2.circle(frame, (x2,y2), 10, (255,0,0), cv2.FILLED)
            cv2.circle(frame, (x3,y3), 10, (255,0,0), cv2.FILLED)
            #cv2.putText(frame, str(int(angle)),(x2-70,y2+20),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        ##
        
        return angle
    ##
    
    # Calculate angle for pose inclination
    def findAngleTwoCoordinates(self,frame,i1,i2, draw = True):
        
        # To get the coordinates/landmarks of 2 points
        x1,y1 = self.coordinates[i1][1:]
        x2,y2 = self.coordinates[i2][1:]
        ##
        
        theta = math.acos( (y2 -y1)*(-y1) / (math.sqrt(
            (x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
        angle = int(180/math.pi)*theta
        
        # Connect all the landmarks with the coordinates into each frame
        if draw:
            cv2.line(frame, (x1,y1),(x2,y2),(255,0,0),3)
            cv2.circle(frame, (x1,y1), 10, (255,0,0), cv2.FILLED)
            cv2.circle(frame, (x2,y2), 10, (255,0,0), cv2.FILLED)
            #cv2.putText(frame, str(int(angle)),(x2-70,y2+20),                           cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        ##
        
        return angle
    ##
    
    # Calculate the distance between two points
    def findDistanceTwoCoordinates(self, frame, i1, i2, draw = True):
        
        # To get the coordinates/landmarks of 2 points
        x1,y1 = self.coordinates[i1][1:]
        x2,y2 = self.coordinates[i2][1:]
        ##
        
        dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
        
        # Connect all the landmarks with the coordinates into each frame
        if draw:
            cv2.line(frame, (x1,y1),(x2,y2),(255,0,0),3)
            cv2.circle(frame, (x1,y1), 10, (255,0,0), cv2.FILLED)
            cv2.circle(frame, (x2,y2), 10, (255,0,0), cv2.FILLED)
            #cv2.putText(frame, str(int(dist)),(x2-70,y2+20),                        cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
        ##
        
        return dist
    ##
    
# Main Function
def main():

    # Video as input for the initiating the estimation
    video = cv2.VideoCapture('Pose Estimation/pose2.avi')
    ##
    
    # Creating an object for the postestimation for reuse the logic of 
    # angle estimation, to fetch and detect the coordinates of each frame
    pEstimate = poseEstimation()
    ##

    # Looping through each frame of the video
    while True:
        # Checking whether the frame has valid image and getting 
        # the current frame
        sucess, frame = video.read()
        ##
        
        # Main checkpoint to verify whether the frame obtained is not none
        # mainly to avoid the assertion error while in the end of the video
        # if no frame is left the window opened are closed
        if frame is not None:
        
            # Resizing the video
            frame = cv2.resize(frame, (1100,820))
            ##
            
            # Detecting the coordinates of each frame and storing back as frame
            # for further estimation
            detector = pEstimate.detectCoordinates(frame)
            ##
            
            # Fetching each coordinates for each frame to determine the angle for 
            # the estimation
            coordinates = pEstimate.findCoordinates(detector, draw=False)
            ##
            
            # Looping through the array of coordination for the detected 
            # coordinates
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
            ##
            
            # Display the coordinates in each frame
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


# When importing this file as Module this will be ignored else main function 
# will be called
if __name__ == "__main__":
    main()
##