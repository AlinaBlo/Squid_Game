from configparser import ConfigParser
import numpy as np

file ='config.ini'
config = ConfigParser()
config.read(file)

config.sections()
dataB=config['setUP']
dataP=config['PoseConf']

setWidth=int(dataB["setWidth"])
setHeight=int(dataB["setHeight"])
beginOfArray=int(dataB["beginOfArray"])
initialTime=int(dataB["initialTime"])
defaultCamera=int(dataB["defaultCamera"])
flipCam=int(dataB["flipCam"])
dCon=float(dataB["dCon"])
tCon=float(dataB["tCon"])
WidthCam=int(dataB["WidthCam"])
HeightCam=int(dataB["HeightCam"])
model_sel=int(dataB["model_sel"])
FrameArray=int(dataB["FrameArray"])

backgrounds=dataB["backgrounds"]

tshold=float(dataB["tshold"])
empty=int(dataB["empty"])

left_hand=np.array(dataB["left_hand"])
right_hand=np.array(dataB["right_hand"])
left_foot=np.array(dataB["left_foot"])
right_foot=np.array(dataB["right_foot"])
head=np.array(dataB["head"])
left_arm=np.array(dataB["left_arm"])
right_arm=np.array(dataB["right_arm"])
left_leg=np.array(dataB["left_leg"])
right_leg=np.array(dataB["right_leg"])

mode=bool(dataP["mode"])
modelposecomplexity=int(dataP["modelposecomplexity"])
smooth=bool(dataP["smooth"])
enablesegmentation = bool(dataP["enablesegmentation"])
smoothsegmentation = bool(dataP["smoothsegmentation"])
detectionCon=float(dataP["detectionCon"])
trackCon=float(dataP["trackCon"])