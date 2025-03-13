import json
import github
import http
from github import UnknownObjectException, GithubException, Branch
from time import sleep

FAIL_COLOR = '\033[91m'
WARNING_COLOR = '\033[33m'
END_COLOR = '\033[0m'

HOST_GITHUB_API = "api.github.com"

def print_fail(message):
    print(FAIL_COLOR + message + END_COLOR)

def print_warning(message):
    print(WARNING_COLOR + message + END_COLOR)

def create_repo_with_settings(user_object, name, is_private=False, create_readme=False, template=False,
                              github_object=False, branch_protection=False):
    sleep(0.05)
    try:
        repo_object = user_object.get_repo(name)
        print_warning("{} exists, skipping create".format(name))
    except UnknownObjectException:
        print("creating repo {}; private:{}; readme:{}".format(name, is_private, create_readme))
        try:
            if not template:
                repo_object = user_object.create_repo(name, private=is_private, auto_init=create_readme)
            else:
                try:
                    repo_owner, repo = template.split('/')
                    template_user_object = get_user_object(github_object, repo_owner)
                    repo_object = user_object.create_repo_from_template(name, private=is_private,
                                                                        repo=template_user_object.get_repo(repo))
                except Exception as e:
                    print_fail("error '{}' with creating repo {} from template {}".format(e, name, template))
                    print_fail("Stop")
                    exit(1)

            if type(branch_protection) is str:
                #repo_object.get_branch(branch_protection).edit_protection(lock_branch=True)
                pass

            print("done")
        except GithubException as e:
            error = str(e.data['errors'][0]['message'])
            print_fail("error '{}' with creating repo {}".format(error, name))
            return False

    return repo_object


def give_an_access(repo_object, collaborator, pull=False, admin=False):
    access = 'admin ' * admin + 'read ' * pull + 'write'
    print("adding {} to collaborators. access: {}".format(collaborator, access.split()[0]))
    sleep(0.05)
    try:
        if admin:
            repo_object.add_to_collaborators(collaborator, permission='admin')
        elif pull:
            repo_object.add_to_collaborators(collaborator, permission='pull')
        else:
            repo_object.add_to_collaborators(collaborator)
    except UnknownObjectException:
        print_fail("ERROR! {} login contains errors, skipping".format(collaborator))

        return False

    return True


def remove_an_access(repo_object, collaborator):
    print("remove {} from collaborators ...".format(collaborator))
    try:
        repo_object.remove_from_collaborators(collaborator)
    except:
        print("Collaborator {} does not exist or waits for invite".format(collaborator))


def change_an_access(users, user_object, repo, give, pull=False, admin=False):
    repo_object = create_repo_with_settings(user_object, name=repo)

    if not repo_object:
        return False

    for user in users:
        if give:
            give_an_access(repo_object, user, pull, admin)
        else:
            remove_an_access(repo_object, user)


def get_user_object(github_object, repo_owner):
    try:
        user = github_object.get_organization(repo_owner)
    except UnknownObjectException:
        user = github_object.get_user()
    return user

def token_probe_reqest(access_token):
    conn = http.client.HTTPSConnection(HOST_GITHUB_API)

    headers = {
        "Authorization": "Bearer {}".format(access_token),
        "User-Agent": "Python-http.client",
        "Accept" : "application/vnd.github+json"
    }

    try:
        conn.request("GET", "/user", headers=headers)

        return conn.getresponse().status

    except http.client.HTTPException as e:
        print_fail("error '{}' with requesting user by token".format(e))

    finally:
        conn.close()

def get_token_from_file(token_path):
    try:
        with open(token_path) as f:
            token = f.readline().rstrip()

        return token
    
    except FileNotFoundError as e:
        print_fail("error '{}'".format(e))
        exit(1)

def auth(token_path):
    token = get_token_from_file(token_path)

    token_status = token_probe_reqest(token)

    if token_status == http.HTTPStatus.OK:
        auth_token = github.Auth.Token(token)
        github_object = github.Github(auth=auth_token)

        print("Authorization succeed")

        return github_object
    else:
        print_fail("Authorization failed: Bad Credentials. Token status is {}".format(token_status))
        exit(1)

