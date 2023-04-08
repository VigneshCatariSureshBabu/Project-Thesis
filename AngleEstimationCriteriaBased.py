# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 00:09:02 2022

@author: Vignesh
"""
# Importing libraries
import cv2
import PoseEstimationModule as pm

def main(video, pEstimate, finalCheck, partSelection,viewSelection = 0,rotate = False):
    
    
    maxr = 0
    maxl = 0
    maxrt = 0
    maxlt = 0
    
    def angleDisplay(text, angle,coordinate1 = (30,50), 
                  coordinate2 = (30,120)):
        #cv2.rectangle(frame, (0, 150), (1280, 0), (0, 0, 0), cv2.LINE_AA)
        cv2.putText(frame, str(text), coordinate1, 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
        
        cv2.putText(frame, str(angle), coordinate2, 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 10)
        
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
            if partSelection == 4:
                frame = cv2.resize(frame, (900, 900))
                # Rotating the video if required
                if rotate:
                    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            elif partSelection == 1 or partSelection == 3:
                if viewSelection != 3:
                    frame = cv2.resize(frame, (900, 820))
                    # Rotating the video if required
                    if rotate:
                        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                else:
                    frame = cv2.resize(frame, (1280, 720))
            else:
                frame = cv2.resize(frame, (1280, 720))
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
                # Knee Flexion
                if partSelection == 1:
                    
                    if viewSelection == 1:
                        # Angle for Right Side Leg
                        angleRightBottom = pEstimate.toFindAngleThreeCoordinates(frame, 24, 26, 28, True)
                        if maxr < abs(round(angleRightBottom - 180)):
                            maxr = abs(round(angleRightBottom - 180))
                        else:
                            maxr = maxr
                        angleDisplay('Knee flexion: Right' , abs(round(angleRightBottom - 180)),(30,50),(30,120))
                        angleDisplay('Maximum Knee Displacement: Right' , maxr,(340,50),(340,120))
                        
                    elif viewSelection == 2:
                        # Angle for Left Side Leg
                        angleLeftBottom = pEstimate.toFindAngleThreeCoordinates(frame, 23, 25, 27, True)
                        if maxl < abs(round(angleLeftBottom -180)):
                            maxl = abs(round(angleLeftBottom -180))
                        else:
                            maxl = maxl
                        angleDisplay('Knee flexion: Left' , abs(round(angleLeftBottom -180)),(30,50),(30,120))
                        angleDisplay('Maximum Knee Displacement: Left ' , maxl,(340,50),(340,120))
                        
                    else:    
                        # Angle for Left Side Leg
                        angleLeftBottom = pEstimate.toFindAngleThreeCoordinates(frame, 23, 25, 27, True)
                        # Angle for Right Side Leg
                        angleRightBottom = pEstimate.toFindAngleThreeCoordinates(frame, 24, 26, 28, True)
                        if maxl < abs(round(angleLeftBottom -180)):
                            maxl = abs(round(angleLeftBottom -180))
                        else:
                            maxl = maxl
                        if maxr < abs(round(angleRightBottom - 180)):
                            maxr = abs(round(angleRightBottom - 180))
                        else:
                            maxr = maxr
                        angleDisplay('Knee flexion: Left' , abs(round(angleLeftBottom -180)),(30,50),(30,120))
                        angleDisplay('Knee flexion: Right' , abs(round(angleRightBottom - 180)),(340,50),(340,120))
                        angleDisplay('Maximum Knee Displacement: Left ' , maxl,(640,50),(640,120))
                        angleDisplay('Maximum Knee Displacement: Right' , maxr,(940,50),(940,120))
                ##
                # Hip Flexion
                elif partSelection == 2:
                    # Angle for Left Side Thigh
                    angleLeftThigh = pEstimate.findAngleTwoCoordinates(frame, 23, 25, True)
                    # Angle for Right Side Thigh
                    angleRightThigh = pEstimate.findAngleTwoCoordinates(frame, 24, 26, True)
                    if maxl < abs(round(angleLeftThigh - 180)):
                        maxl = abs(round(angleLeftThigh - 180))
                    else:
                        maxl = maxl
                    if maxr < abs(round(angleRightThigh - 180)):
                        maxr = abs(round(angleRightThigh - 180))
                    else:
                        maxr = maxr
                    angleDisplay('Hip flexion: Left' , abs(round(angleLeftThigh - 180)),(30,50),(30,120))
                    angleDisplay('Hip flexion: Right' , abs(round(angleRightThigh - 180)),(340,50),(340,120))
                    angleDisplay('Maximum Hip Displacement: Left ' , maxl,(640,50),(640,120))
                    angleDisplay('Maximum Hip Displacement: Right' , maxr,(940,50),(940,120))
                ##
                # Trunk Flexion
                elif partSelection == 3:
                    if viewSelection == 1:
                        # Angle for Right Side Trunk
                        angleRightTrunk = pEstimate.toFindAngleThreeCoordinates(frame, 12, 24,26, True)
                        if maxr == 0:
                            maxr = round(angleRightTrunk)
                        else:  
                            if maxr > abs(round(angleRightTrunk)):
                                maxr = abs(round(angleRightTrunk))
                            else:
                                maxr = maxr
                        angleDisplay('Trunk flexion' , (round(angleRightTrunk)),(30,50),(30,120))
                        angleDisplay('Maximum Hip Displacement: Right' , maxr,(340,50),(340,120))
                    elif viewSelection == 2:
                        # Angle for Left Side Trunk
                        angleLeftTrunk = pEstimate.toFindAngleThreeCoordinates(frame, 11, 23, 25, True)
                        if maxl == 0:
                            maxl = round(360- angleLeftTrunk)
                        else:
                            if maxl > abs(round(360 - angleLeftTrunk)):
                                maxl = abs(round(360 - angleLeftTrunk))
                            else:
                                maxl = maxl
                        angleDisplay('Trunk flexion' , (round(360 - angleLeftTrunk)),(30,50),(30,120))
                        angleDisplay('Maximum Hip Displacement: Left ' , maxl,(340,50),(340,120))
                    else:
                        # Angle for Left Side Trunk
                        angleLeftTrunk = pEstimate.toFindAngleThreeCoordinates(frame, 11, 23, 25, True)
                        # Angle for Right Side Trunk
                        angleRightTrunk = pEstimate.toFindAngleThreeCoordinates(frame, 12, 24, 26, True)
                        # if maxl < abs(round(angleLeftTrunk - 180)):
                        #     maxl = abs(round(angleLeftTrunk - 180))
                        # else:
                        #     maxl = maxl
                        # if maxr < abs(round(angleRightTrunk - 180)):
                        #     maxr = abs(round(angleRightTrunk - 180))
                        # else:
                        #     maxr = maxr
                        angleDisplay('Trunk flexion: Left' , (round(angleLeftTrunk)),(30,50),(30,120))
                        angleDisplay('Trunk flexion: Right' , (round(angleRightTrunk)),(340,50),(340,120))
                        # angleDisplay('Maximum Hip Displacement: Left ' , maxl,(640,50),(640,120))
                        # angleDisplay('Maximum Hip Displacement: Right' , maxr,(940,50),(940,120))
                ##
                # Ankle Plantar Flexion
                elif partSelection == 4:
                    if viewSelection == 1:
                        angleRightAnkle = pEstimate.toFindAngleThreeCoordinates(frame, 26,28,32, True)
                        absAngleRightAnkle = (round(angleRightAnkle - 90,2))
                        angleDisplay("Ankle Plantar flexion: Right", absAngleRightAnkle,(30,50),(30,120))
                    else:
                        angleLeftAnkle = pEstimate.toFindAngleThreeCoordinates(frame, 25,27,31, True)
                        absAngleLeftAnkle = (round(270- angleLeftAnkle,2))
                        angleDisplay("Ankle Plantar flexion: Left", absAngleLeftAnkle,(30,50),(30,120))
                    
                ##
                
                # Medial knee positon
                elif partSelection == 5:
                    angleLeftMedialKnee = pEstimate.findAngleTwoCoordinates(frame, 25,27, True)
                    angleRightMedialKnee = pEstimate.findAngleTwoCoordinates(frame, 26,28, True)
                    angleDisplay('Medial Knee: Left' , abs(round(angleLeftMedialKnee-180)),(30,50),(30,120))
                    angleDisplay('Medial knee: Right' , abs(round(angleRightMedialKnee-180)),(340,50),(340,120))
                ##
                # Lateral Trunk Flexion
                elif partSelection == 6:
                        angleRightLateralTrunk = pEstimate.findAngleTwoCoordinates(frame, 12, 24, True)
                        absAngleRightLateralTrunk = abs(round(angleRightLateralTrunk - 170))
                        angleDisplay("Lateral Trunk flexion: Right", absAngleRightLateralTrunk,(520,50),(520,120))
                        angleLeftLateralTrunk = pEstimate.findAngleTwoCoordinates(frame, 11, 23, True)
                        absAngleLeftLateralTrunk = abs(round(angleLeftLateralTrunk - 170))
                        angleDisplay("Lateral Trunk flexion: Left", absAngleLeftLateralTrunk,(30,50),(30,120))
                ##
                # Stance width
                elif partSelection == 7:
                    footDistance = pEstimate.findDistanceTwoCoordinates(frame, 31, 32, True)
                    angleDisplay('Foot width' , round(footDistance), (30,50),(30,120))
                    shoulderWidth = pEstimate.findDistanceTwoCoordinates(frame, 11, 12, True)
                    angleDisplay('Shoulder width' , round(shoulderWidth),(340,50),(340,120))
                    
                    if footDistance > shoulderWidth:
                        cv2.putText(frame, "Foot is wider than shoulder", (640,50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
                    elif footDistance == shoulderWidth:
                        cv2.putText(frame, "Foot and shoulder is verticle to ground", (640,50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
                    else:
                        cv2.putText(frame, "Foot is narrow than shoulder", (640,50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 204, 102), 5)
                ##
                # Foot position
                elif partSelection == 8:
                    # Angle for Left Side Ankle
                    angleLeftAnkle = pEstimate.findAngleTwoCoordinates(frame, 29,31, True)
                    if round(angleLeftAnkle)-180 > 0:
                        angleDisplay(
                            'Foot position - Left : Internal Rotation',
                            abs(round(angleLeftAnkle)-180),(30,50),(30,120))
                    elif round(angleLeftAnkle)-180 < 0:
                        angleDisplay(
                            'Foot position - Left : External Rotation',
                            abs(round(angleLeftAnkle)-180),(30,50),(30,120))
                    else:
                        angleDisplay(
                            'Foot position - Left : No Rotation',
                            abs(round(angleLeftAnkle)-180),(30,50),(30,120))
                    # Angle for Right Side Ankle
                    angleRightAnkle = pEstimate.findAngleTwoCoordinates(
                        frame, 30,32, True)
                    if round(angleRightAnkle)-180 > 0:
                        angleDisplay(
                            'Foot position - Right : Internal Rotation',
                            abs(round(angleRightAnkle)-180),(30,150),(30,220))
                    elif round(angleRightAnkle)-180 < 0:
                        angleDisplay(
                            'Foot position - Right : External Rotation',
                            abs(round(angleRightAnkle)-180),(30,150),(30,220))
                    else:
                        angleDisplay(
                            'Foot position - Right : No Rotation',
                            0,(30,150),(30,220))
                ##
                # Symmetric foot contact
                elif partSelection == 9:
                    angleSymmetricalAnkels = pEstimate.findAngleTwoCoordinates(frame, 27, 28, True)
                    angleSymmetricalToes = pEstimate.findAngleTwoCoordinates(frame, 31, 32, True)
                    angleSymmetricalHeels = pEstimate.findAngleTwoCoordinates(frame, 29, 30, True)
                    angleDisplay('Ankles Symmatry' , abs(round(angleSymmetricalAnkels-90)),(30,50),(30,120))
                    angleDisplay('Toes Symmetry' , abs(round(angleSymmetricalToes-90)),(340,50),(340,120))
                    angleDisplay('Heels Symmetry' , abs(round(angleSymmetricalHeels-90)),(640,50),(640,120))
                ##
                # Joint displacement
                elif partSelection == 10:
                   # angleHip = pEstimate.findAngleTwoCoordinates(frame, 23, 24, True)
                   # angleShoulder =pEstimate.findAngleTwoCoordinates(frame, 11, 12, True)
                   # angleKnee = pEstimate.findAngleTwoCoordinates(frame, 25, 26, True)
                   # angleDisplay('Hip displacement' , abs(round(angleHip-90)),(30,50),(30,120))
                   # angleDisplay('Shoulder displacement' , abs(round(angleShoulder-90)),(340,50),(340,120))
                   # angleDisplay('Knee displacement' , abs(round(angleKnee-90)),(740,50),(740,120)) 
                   
                   # OR
                   # Angle for Left Part of the Body
                   angleLeftTop = pEstimate.toFindAngleThreeCoordinates(frame, 11, 23, 25, True)
                   # Angle for Right Part of the Body
                   angleRightTop = pEstimate.toFindAngleThreeCoordinates(frame, 12, 24, 26, True)
                   if maxlt < abs(round(angleLeftTop -180)):
                       maxlt = abs(round(angleLeftTop -180))
                   else:
                       maxlt = maxlt
                   if maxrt < abs(round(angleRightTop - 180)):
                       maxrt = abs(round(angleRightTop - 180))
                   else:
                       maxrt = maxrt
                   angleDisplay('Maximum Trunk Displacement: Left ' , maxl,(30,50),(30,120))
                   angleDisplay('Maximum Trunk Displacement: Right' , maxr,(640,50),(1140,120))   
                   # Angle for Left Side Leg
                   angleLeftBottom = pEstimate.toFindAngleThreeCoordinates(frame, 23, 25, 27, True)
                   # Angle for Right Side Leg
                   angleRightBottom = pEstimate.toFindAngleThreeCoordinates(frame, 24, 26, 28, True)
                   if maxl < abs(round(angleLeftBottom -180)):
                       maxl = abs(round(angleLeftBottom -180))
                   else:
                       maxl = maxl
                   if maxr < abs(round(angleRightBottom - 180)):
                       maxr = abs(round(angleRightBottom - 180))
                   else:
                       maxr = maxr
                   angleDisplay('Maximum Knee Displacement: Left ' , maxl,(30,150),(30,220))
                   angleDisplay('Maximum Knee Displacement: Right' , maxr,(640,150),(1140,220))   
                   #####
                ##
                # Close all the windows
                else:
                    cv2.destroyAllWindows()
                    break
    
            # Display the result text in each frame
            cv2.imshow("Pose Estimation", frame)   
            ##
        
            # Breaking the loop to close the window by pressing 'q' key
            # Masking the 28 bit of key pressed with the unique code
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            ##
            elif cv2.waitKey == ord('p'):
                cv2.waitKey()
            
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
    
    finalCheck = ['leftBottom', 'rightBottom', 'leftTop', 'rightTop']
    
    
    ##
    
    # Creating an object for the postestimation for reuse the logic of 
    # angle estimation, to fetch and detect the coordinates of each frame
    pEstimate = pm.poseEstimation()
    ##
    partSelection = int(input(
        "Enter the number for evaluate: 1. Knee Flexion, 2. Hip Flexion, 3. Trunk Flexion, 4. Ankle Plantar Flexion, 5. Medial knee positon, 6. Lateral Trunk Flexion, 7. Stance width, 8. Foot position, 9. Symmetric foot contact, 10. Joint displacement:\n"))
    
    if partSelection == 4:
        viewSelection = int(input(
            "Enter the number for view for evaluation: 1. Right Side View, 2. Left Side View:\n"))
        if viewSelection == 1:
            # Video as input for the initiating the estimation in Right side
            video = cv2.VideoCapture('Pose Estimation/016/Dop Jump 1/Drop Jump Bilateral Markerless 1_Miqus_6_25467.avi')
        else:
            # Video as input for the initiating the estimation in left side
            video = cv2.VideoCapture('Pose Estimation/016/Dop Jump 1/Drop Jump Bilateral Markerless 1_Miqus_10_25459.avi')
        ##
        # Calling the main function
        main(video, pEstimate, finalCheck, partSelection, viewSelection, True)
    elif partSelection == 1 or partSelection == 3:
        
        viewSelection = int(input(
            "Enter the number for view for evaluation: 1. Right Side View, 2. Left Side View:\n"))
        if viewSelection == 1:
            rotation = True
            # Video as input for the initiating the estimation in Right side
            video = cv2.VideoCapture('Pose Estimation/020/Dop Jump 1/Drop Jump Bilateral Markerless 1_Miqus_6_25467.avi')
        elif viewSelection == 2:
            rotation = True
            # Video as input for the initiating the estimation in left side
            video = cv2.VideoCapture('Pose Estimation/020/Dop Jump 1/Drop Jump Bilateral Markerless 1_Miqus_10_25459.avi')
            
        else:
            rotation = False
            # Video as input for the initiating the estimation
            video = cv2.VideoCapture('Pose Estimation/020/Dop Jump 1/Drop Jump Bilateral Markerless 1_Miqus_3_25465.avi')
        # Calling the main function
        main(video, pEstimate, finalCheck, partSelection, viewSelection, rotation)
        ##
    else:
        # Video as input for the initiating the estimation
        video = cv2.VideoCapture('Pose Estimation/020/Dop Jump 1/Drop Jump Bilateral Markerless 1_Miqus_3_25465.avi')
    
        # Calling the main function
        main(video, pEstimate, finalCheck, partSelection)
        ##
##