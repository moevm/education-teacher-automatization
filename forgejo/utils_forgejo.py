import json
import requests
import time
from requests.exceptions import HTTPError

FAIL_COLOR = '\033[91m'
WARNING_COLOR = '\033[33m'
END_COLOR = '\033[0m'

FORGEJO_HOST = "git.moevm.info"
FORGEJO_API_BASE = f"https://{FORGEJO_HOST}/api/v1"

def print_fail(message):
    print(FAIL_COLOR + message + END_COLOR)

def print_warning(message):
    print(WARNING_COLOR + message + END_COLOR)

def create_repo_with_settings_forgejo(session, owner, name, is_private=False, create_readme=False, template=None, branch_protection=None):
    repo_url = f"{FORGEJO_API_BASE}/repos/{owner}/{name}"
    response = session.get(repo_url)
    if response.status_code == 200:
        print_warning(f"{owner}/{name} exists, skipping create")
        return response.json()
    
    create_data = {
        "name": name,
        "private": is_private,
        "auto_init": create_readme,
        "description": f"Repository {name} in {owner}"
    }
    
    if template:
        template_owner, template_repo = template.split('/')
        create_url = f"{FORGEJO_API_BASE}/repos/{template_owner}/{template_repo}/generate"
        create_data["owner"] = owner
        response = session.post(create_url, json=create_data)
    else:
        create_url = f"{FORGEJO_API_BASE}/orgs/{owner}/repos"
        response = session.post(create_url, json=create_data)
        if response.status_code not in [201, 200]:
            error = response.json().get('message', 'Unknown error')
            print_fail(f"Error creating repo in organization {owner}/{name}: {error}")
            return None
    
    if response.status_code in [201, 200]:
        repo_data = response.json()
        actual_owner = repo_data['owner']['login']
        print(f"Created repo {actual_owner}/{name}")
        return repo_data
    
    error = response.json().get('message', 'Unknown error')
    print_fail(f"Error creating repo {owner}/{name}: {error}")
    return None

def give_an_access_forgejo(session, owner, repo, collaborator, permission='write'):
    url = f"{FORGEJO_API_BASE}/repos/{owner}/{repo}/collaborators/{collaborator}"
    data = {"permission": permission}
    response = session.put(url, json=data)
    
    if response.status_code == 204:
        print(f"Added {collaborator} to {owner}/{repo} with {permission} access")
        return True
    else:
        error = response.json().get('message', 'Unknown error')
        print_fail(f"Error adding {collaborator}: {error}")
        return False

def remove_an_access_forgejo(session, owner, repo, collaborator):
    url = f"{FORGEJO_API_BASE}/repos/{owner}/{repo}/collaborators/{collaborator}"
    response = session.delete(url)
    
    if response.status_code == 204:
        print(f"Removed {collaborator} from {owner}/{repo}")
        return True
    else:
        print(f"Collaborator {collaborator} not found or already removed")
        return False

def change_an_access_forgejo(session, users, owner, repo, give, pull=False, admin=False):
    if admin:
        permission = 'admin'
    elif pull:
        permission = 'read'
    else:
        permission = 'write'
    for user in users:
        if give:
            give_an_access_forgejo(session, owner, repo, user, permission)
        else:
            remove_an_access_forgejo(session, owner, repo, user)

def token_probe_request_forgejo(session):
    response = session.get(f"{FORGEJO_API_BASE}/user")
    return response.status_code

def get_token_from_file_forgejo(token_path):
    try:
        with open(token_path) as f:
            return f.read().strip()
    except FileNotFoundError:
        print_fail(f"Token file not found: {token_path}")
        exit(1)

def auth_forgejo(token_path):
    token = get_token_from_file_forgejo(token_path)
    session = requests.Session()
    session.headers.update({
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    })
    
    if token_probe_request_forgejo(session) == 200:
        print("Authorization successful")
        return session
    
    print_fail("Authorization failed: Invalid token")
    exit(1)
    