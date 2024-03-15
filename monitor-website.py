import requests
import smtplib
import os

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

response = requests.get('http://104.236.6.212:8080/')
if response.status_code == 200:
    print('app running successfully')
else:
    print('app need to be fix it')
    
    #send email using gmail account
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = "Subject: app not available\nRestart the application."
        smtp.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,msg)
