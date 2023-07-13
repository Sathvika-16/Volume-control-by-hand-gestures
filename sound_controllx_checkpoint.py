import cv2
import mediapipe as mp
from mediapipe.python.solutions.drawing_utils import draw_landmarks
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#volume.GetMasterVolumeLevel()

capturing = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
myhands = mpHands.Hands()
Drawing = mp.solutions.drawing_utils

while True:
    success , imgage =capturing.read()
    img1 = cv2.cvtColor(imgage , cv2.COLOR_BGR2RGB)
    output = myhands.process(img1)
    #print(results.multi_hand_landmarks)

    if output.multi_hand_landmarks:
        for handLms in output.multi_hand_landmarks:
            lmList = []
            for id ,lm in enumerate(handLms.landmark):
                #print(id , lm)
                h ,w , c = imgage.shape
                cx ,cy = int(lm.x*w) , int(lm.y*h)
                lmList.append([id ,cx, cy])

                Drawing.draw_landmarks(imgage , handLms ,mpHands.HAND_CONNECTIONS)
            
        if lmList:
            x1 ,y1  = lmList[4][1] , lmList[4][2]
            x2, y2  = lmList[8][1], lmList[8][2]
            cv2.circle(imgage , (x1, y1) , 15 ,(255,0,0) , cv2.FILLED )
            cv2.circle(imgage , (x2, y2) , 15 ,(255,0,0) , cv2.FILLED )
            cv2.line(imgage , (x1 , y1) , (x2 , y2) ,(255 , 0 , 255) , 3)

            z1 , z2 = (x1+x2)//2 , (y1+y2)//2
            length = math.hypot(x2- x1 , y2- y1)
            if length<50 :
                cv2.circle(imgage , (z1 ,z2) ,15 , (255 , 255 , 255) ,cv2.FILLED)
            
            #print(length)
            
            #volume.GetMute()
        volumeRange  = volume.GetVolumeRange()
        minimunVol = volumeRange[0]
        maximumVol = volumeRange[1]
        vollume = numpy.interp(length , [50 ,300] , [minimunVol ,maximumVol])
        volumeBar = numpy.interp(length , [50 ,300] , [400 ,150])
        volumePer = numpy.interp(length , [50 ,300] , [0 ,100])

        #length =50  ===> volumePer =0
        #length = 300 ===>volumePer =100
        #length = 175 ==> volumePer = 50
        #print(vollume)
        #print(int(length) , vollume)
        #print(minimunVol ,maximumVol)
        volume.SetMasterVolumeLevel(vollume, None)
        cv2.rectangle(imgage , (50 ,150) , (85 , 400) ,(123,213,122) ,3)
        cv2.rectangle(imgage , (50 , int(volumeBar)) , (85 ,400) ,(0, 231,23) ,cv2.FILLED)
        cv2.putText(imgage , str(int(volumePer)) , (40, 450) ,cv2.FONT_HERSHEY_PLAIN ,4 , (24,34,34) , 3)
        

    cv2.imshow("Image" ,imgage)
    cv2.waitKey(1)




# Length of line ===50, 300
# Range of sound is ===-21, 20
# Range of actual volume === 0,100