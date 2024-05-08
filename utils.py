import json
import github
from github import UnknownObjectException, GithubException, Branch
from time import sleep

FAIL_COLOR = '\033[91m'
WARNING_COLOR = '\033[33m'
END_COLOR = '\033[0m'


def create_repo_with_settings(user_object, name, is_private=False, create_readme=False, template=False,
                              github_object=False, branch_protection=False):
    sleep(0.05)
    try:
        repo_object = user_object.get_repo(name)
        print(WARNING_COLOR + "{} exists, skipping create".format(name) + END_COLOR)
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
                    print(FAIL_COLOR + "error '{}' with creating repo {} from template {}".format(e, name, template) + END_COLOR)
                    print(FAIL_COLOR + "Stop" + END_COLOR)
                    exit(1)

            if type(branch_protection) is str:
                #repo_object.get_branch(branch_protection).edit_protection(lock_branch=True)
                pass

            print("done")
        except GithubException as e:
            error = str(e.data['errors'][0]['message'])
            print(FAIL_COLOR + "error '{}' with creating repo {}".format(error, name) + END_COLOR)
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
        print((FAIL_COLOR + "ERROR! {} login contains errors, skipping" + END_COLOR).format(
            collaborator))

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
        user = github_object.get_user(repo_owner)
    return user


def auth(access_token):
    try:
        github_object = github.Github(access_token)
        print("Authorization succeed")
        print(github_object.__dict__)
        return github_object
    except Exception as e:
        print("Authorization failed. Error:{}".format(e))
        exit(1)
