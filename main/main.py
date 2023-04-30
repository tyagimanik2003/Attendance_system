import cv2
import numpy as np
import pandas as pd
import face_recognition
import requests
from requests.auth import HTTPBasicAuth
import imutils
from datetime import datetime
import os


path = 'Image_Attendance'
images = []
classNames = []
myList = os.listdir(path)
today = datetime.now().strftime("%d-%m-%Y")

for cls in myList:
    curImg =  cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])

print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnow = findEncodings(images)
print('Encoding Complete')


def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            f.writelines(f'\n{name},{today}')
  

url = "http://192.168.50.74:8080/shot.jpg"
username = "ABC"
password = "abc"
pTime=0

imgBG = cv2.imread('Resources/mainpage.png')

while True:
    img_resp = requests.get(url, auth = HTTPBasicAuth(username, password))
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv2.imdecode(img_arr, -1)
    img = imutils.resize(img, width=640, height=480)
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    imgBG[ 120: 120 + 480, 561:561 + 640 ] = img


    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnow,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)
        if(faceDis[matchIndex]>0.45):
            continue

        if matches[matchIndex]:
            
            name = classNames[matchIndex].upper()
            print(name)
            markAttendance(name)
    
    cv2.imshow('Andriod Cam',imgBG)
    if cv2.waitKey(1) == ord('q'):
        break
  
cv2.destroyAllWindows()

# For Showing Total Present + list of absentees
df=pd.read_csv("Attendance.csv")
data=df['Name']
print("Total students Present : ",len(data))



# For sending automated mails.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

sender_address = ''
sender_pass = ''
    
subject=f'Attendance record for {today}'
mail_content = '''
Students kindly check todays attendance report.
'''

# Read the CSV file into a DataFrame
dt=pd.read_csv("Students.csv")
data=dt["Outlook Mail ID"]

for i in data:
    receiver_address=i
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Attendance record'
    message.attach(MIMEText(mail_content, 'plain'))
    df=pd.read_csv("Attendance.csv")
    # create a CSV string from the DataFrame
    csv_string = df.to_csv(index=False)
    # convert the string to a MIME attachment
    attachment = MIMEBase("text", "csv")
    attachment.set_payload(csv_string.encode())
    encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename="Attendance.csv")
    message.attach(attachment)
    
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

print('Mail Sent')

