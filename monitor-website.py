import requests #package for make requests
import smtplib #package for sending emails
import os #package for use enviroment variables
import paramiko #package for sshing
import json #package to work with JSON data
import time #package to work with built in function of time
import schedule

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DOTOKEN = os.environ.get('DOTOKEN')

#function to send email using gmail account
def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        message = f"Subject: app not available\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS,message)

#function to restart the app
def restart_container():
    ssh = paramiko.SSHClient()
    ssh.net_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=xxx, username=xxx, key_filename=xxx)
    stdin, stdout, stderr = ssh.exec_command('docker start containerid')
    print(stdout.readlines())
    ssh.close()

# function to get the droplet_id from the server name
def get_droplet_info(droplet_name):
    api_url = f'https://api.digitalocean.com/v2/droplets?name={droplet_name}'  #Url that will be used to call API request
    response = requests.get(api_url, headers=headers) #Get the response from API after sending request
    if response.status_code == 200: #If response is success, show the response. Otherwise return nothing
        data = (json.loads(response.content.decode('utf-8')))
        droplet_id = data['droplets'][0]['id']
        return droplet_id

# function to reboot the server from the droplet id    
def reboot_droplet(droplet_id):
    api_droplet_action_url = f'https://api.digitalocean.com/v2/droplets/{droplet_id}/actions' #Url that will be used for API request
    action = {"type":"reboot"} #Gathering necessary information
    requests.post(api_droplet_action_url, headers=headers, json=action) #Sending the gathered information with post request to reboot the droplet

# function to get the server status
def get_droplet_status(droplet_id):
    api_url = f'https://api.digitalocean.com/v2/droplets/{droplet_id}'  #Url that will be used to call API request
    response = requests.get(api_url, headers=headers) #Get the response from API after sending request
    if response.status_code == 200: #If response is success, show the response. Otherwise return nothing
        data = (json.loads(response.content.decode('utf-8')))
        droplet_status = data['droplet']['status']
        return droplet_status    


def restart_server_and_app():
    # restart server
    api_token = DOTOKEN
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_token}'}  # Header information that will be sent to the digitalocean in order to authenticate user
    droplet_name = 'test-droplet'

    droplet_id = get_droplet_info(droplet_name)

    # Reboot the server
    reboot_droplet(droplet_id)

    # restart application
    while True:
        droplet_status = get_droplet_status(droplet_id)
        if droplet_status == 'active':
            time.sleep(5)
            restart_container()
            break

def monitor_application():
    try:
        response = requests.get('http://104.236.6.212:8080/')
        if response.status_code == 200:
            print('app running successfully')
        else:
            print('app need to be fix it')
            msg = f'App returned {response.status_code}'
            send_notification(msg)

            #restart the app
            restart_container()
            
    except Exception as ex:
        print(f'Connection error: {ex}')
        msg = 'App not accessible'
        send_notification(msg)
        restart_server_and_app()


schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run.pending()