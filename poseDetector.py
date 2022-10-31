import cv2
import mediapipe as mp

class poseDetector():
    """MediaPipe Pose.

      MediaPipe Pose processes an RGB image and returns pose landmarks on the most
      prominent person detected.

      Initializes a MediaPipe Pose object
      """

    def __init__(self, mode=False, modelposecomplexity=0,smooth=True,enablesegmentation = False,smoothsegmentation = False,detectionCon=0.0, trackCon=0.0):
        self.mode = mode
        self.modelposecomplexity = modelposecomplexity
        self.smooth=smooth
        self.enablesegmentation = enablesegmentation
        self.smoothsegmentation = smoothsegmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.modelposecomplexity,self.smooth,self.enablesegmentation,self.smoothsegmentation, self.detectionCon, self.trackCon)


    """
    finds the human pose from the image
    """
    def findPose(self, img ,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.resultsp = self.pose.process(imgRGB)
        if self.resultsp.pose_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, self.resultsp.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    """
    Adds the landmarks of the human pose from the image
    """
    def findPosition(self, img, poseNo=0, draw=True):
        lmList = []
        if self.resultsp.pose_landmarks:
            for id, lm in enumerate(self.resultsp.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 100, 100), cv2.FILLED)
        return lmList