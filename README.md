## Website monitoring and recovery on Digital Ocean

Prerequisites: Have an account on Digital Ocean cloud provider.

 ### NGINX CONTAINER

 Step 1: Create a droplet with debian OS and a name as ‘test-droplet’

 Step 2: Connect via ssh to the droplet and install docker engine

 Step 3: Install nginx docker container
Execute on terminal the following command:

    docker run -d -p 8080:80 nginx

### PYTHON SCRIPT FOR MONITORING ON UBUNTU    

Step 4: Install requests python package to make a request to the nginx server.
Execute the following command for ubuntu/debian:

    apt-get install python-requests

Step 5: Set the environment variables permanently on ubuntu os
Execute the following command:

    vim ~/.profile

Add the command to the bottom of the file.
Save and close the file.
Log out and log in again on ubuntu.    