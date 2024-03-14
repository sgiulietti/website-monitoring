import requests
import smtplib

response = requests.get('http://104.236.6.212:8080/')
if response.status_code == 200:
    print('app running successfully')
else:
    print('app need to be fix it')