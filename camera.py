import cv2
from numpy import *
import poseDetector as PD
import statistics
import configFiles as CF

wCam, hCam=CF.WidthCam,CF.HeightCam

#Set Camera frame
cap =cv2.VideoCapture(CF.defaultCamera)
cap.set(CF.setWidth,wCam)
cap.set(CF.setHeight,hCam)

#Set Time values
prevTime=CF.initialTime
Frame_Array=[]

#pose detector info
detector = PD.poseDetector(detectionCon=CF.dCon,trackCon=CF.tCon)

class Camera:
    def __init__(self):
        print("sup")

    # Returns the median
    def Median(self,lst):
        return statistics.median(lst)

    # detects the pose and camera and returns the landmarks and img
    def Pose_And_Camera_Info(self):
        success, img = cap.read()
        img = cv2.resize(img, (wCam, hCam))#1280 720
        img = cv2.cvtColor(cv2.flip(img, CF.flipCam), cv2.COLOR_RGB2BGR)
        img = detector.findPose(img, draw=False)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        landmarks = detector.findPosition(img,draw=False)
        return landmarks, img

    # Returns the Frame Array
    def Lendmarks_To_Array(self,landmarks, Frame_Array):
        if len(landmarks) != CF.empty:
            Frame_Array.append(landmarks)
        return Frame_Array

    # Gets the first and last Frame in the array & returns the distance between the points
    def Find_Velocity_Diff(self,Fram_1, Fram_2):
        VelocityArray = []
        for i, g in enumerate(Fram_1):
            F1, F2 = array(Fram_1[i]), array(Fram_2[i])
            VelocityArray.append(linalg.norm((F1[CF.beginOfArray:]) - (F2[CF.beginOfArray:])))
        return VelocityArray

