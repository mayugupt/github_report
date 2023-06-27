# github_report
This repo is created for GitHub pull requests report.

**Steps to trigger automation via Docker image:**
---
1. Update config.ini with below details

> [repo]
* repository_owner =  
* repository_name = 

> [email]
* sender_email = 
* sender_password = 
* recipient_email = 
* subject = GitHub Pull Requests Report - Last Week
* message = ******* This is an auto-generated report by Python *******

2. Build docker image
* Clone the the github-report repository
* cd github-report
> docker build -t "tag name" .

3. Run docker container
> docker run "image name"
OR
> docker run -e REPOSITORY_OWNER="repository owner" -e \
   REPOSITORY_NAME="repository name" \
   "image name"

4. Alternatively, this application can be run as part of k8s pod using Cronjob resource
