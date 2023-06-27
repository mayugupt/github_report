import requests
import configparser
import os
from datetime import datetime

import notify

# Get pull requests data from GitHub
def get_pull_requests(repo_owner, repo_name, state):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    params = {
        "state": state
    }
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Calculate days between two dates
def calculate_days(created_at_str) -> int:
    today = datetime.now()
    date_object = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
    num_of_days_diff = today - date_object
    num_of_days = num_of_days_diff.days
    return num_of_days

# Get open pull requests
def get_open_pull_requests(repository_owner, repository_name) -> list:
    opened_pull_req_list = []
    count = 0
    open_pull_requests = get_pull_requests(repository_owner, repository_name, "open")
    if open_pull_requests:
        opened_pull_req_list.append("\n\nOpen Pull Requests:")
        for pr in open_pull_requests:
            if calculate_days(pr['created_at']) < 7:
                opened_pull_req_list.append(f"Title: {pr['title']}")
                count += 1
        opened_pull_req_list.append(f"TOTAL: {count}\n")
    return opened_pull_req_list

# Get closed pull requests
def get_closed_pull_requests(repository_owner, repository_name) -> list:
    closed_pull_req_list = []
    count = 0
    closed_pull_requests = get_pull_requests(repository_owner, repository_name, "closed")
    if closed_pull_requests:
        closed_pull_req_list.append("\nClosed Pull Requests:")
        for pr in closed_pull_requests:
            if calculate_days(pr['created_at']) < 7:
                closed_pull_req_list.append(f"Title: {pr['title']}")
                count += 1
        closed_pull_req_list.append(f"TOTAL: {count}\n")
    return closed_pull_req_list

# Get merged pull requests
def get_merged_pull_requests(repository_owner, repository_name) -> list: 
    merged_pull_req_list = []
    count = 0
    merged_pull_requests = get_pull_requests(repository_owner, repository_name, "closed")
    if merged_pull_requests:
        merged_pull_req_list.append("\nMerged Pull Requests:")
        for pr in merged_pull_requests:
            if calculate_days(pr['created_at']) < 7:
                if pr['merged_at']:
                    merged_pull_req_list.append(f"Title: {pr['title']}")
                    count += 1
        merged_pull_req_list.append(f"TOTAL: {count}")
    return merged_pull_req_list

if __name__ == '__main__':

    INITIAL_MESSAGE_LENGTH = 58

    # Create config parser object
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Provide your GitHub repository details - Can be taken as input from user
    if os.environ.get('REPOSITORY_OWNER') and os.environ.get('REPOSITORY_NAME'):
        repository_owner = os.environ.get('REPOSITORY_OWNER')
        repository_name = os.environ.get('REPOSITORY_NAME')
    else:
        repository_owner = config['repo']['repository_owner']
        repository_name = config['repo']['repository_name']

    ### send email - Recipient can be taken as input from user
    sender_email = config['email']['sender_email']
    sender_password = config['email']['sender_password']
    recipient_email = config['email']['recipient_email']
    subject = config['email']['subject']
    message = config['email']['message']

    # Construct message and send email
    message = message + '\n'.join(get_open_pull_requests(repository_owner, repository_name)) \
                + '\n'.join(get_closed_pull_requests(repository_owner, repository_name)) \
                +'\n'.join(get_merged_pull_requests(repository_owner, repository_name))
    
    if len(message) > INITIAL_MESSAGE_LENGTH:
        # Send notification via email to the recipient(s)
        print(f'Email Notification:\n \
            From: {sender_email}\n \
            To: {recipient_email}\n \
            Subject: {subject}\n \
            Body: {message}'
            )
        notify.send_email(sender_email, sender_password, recipient_email, subject, message)