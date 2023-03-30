import cv2
import face_recognition
import numpy as np
import math
import time
cap = cv2.VideoCapture(0)
offset = 20
imgSize = 300
counter = 0

folder = "ImagesData/Z"

while True:
    
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)

    for faceLoc in facesCurFrame:
            # print(name)
            y1,x2,y2,x1 =faceLoc
            y1,x2,y2,x1 =y1*4,x2*4,y2*4,x1*4


            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
    
    cv2.imshow('Webcam',imgBG)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release() 
cv2.destroyAllWindows()
    
    # if hands:
    #     hand = hands[0]
    #     x, y, w, h = hand['bbox']

    #     imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255

    #     imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

    #     imgCropShape = imgCrop.shape

    #     aspectratio = h/w

    #     if aspectratio > 1:
    #         k = imgSize/h
    #         widthCal = math.ceil(k*w)
    #         imgResize = cv2.resize((imgCrop), (widthCal, imgSize))
    #         imgResizeShape = imgResize.shape
    #         widthGap = math.ceil((imgSize-widthCal)/2)
    #         imgWhite[:, widthGap:widthCal+widthGap] = imgResize

    #     else:
    #         k = imgSize/w
    #         heightCal = math.ceil(k*h)
    #         imgResize = cv2.resize((imgCrop), (imgSize, heightCal))
    #         imgResizeShape = imgResize.shape
    #         heightGap = math.ceil((imgSize-heightCal)/2)
    #         imgWhite[heightGap:heightCal+heightGap, :] = imgResize

    #     cv2.imshow("ImageCrop", imgCrop)
    #     cv2.imshow("Imagewhite", imgWhite)

    # cv2.imshow("Image", img)
    # key = cv2.waitKey(1)
    # if key == ord("s"):
    #     counter += 1
    #     cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
    #     print(counter)