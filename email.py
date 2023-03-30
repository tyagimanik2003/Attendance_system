import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

sender_address = 'manikDtyagi@gmail.com'
sender_pass = 'ysouxetslbdzxuir'
    
subject='Attendance record'
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