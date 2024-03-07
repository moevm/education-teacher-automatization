from github import UnknownObjectException
from time import sleep

from grant_access_to_github_repo import FAIL_COLOR, END_COLOR, WARNING_COLOR


def create_repo_with_settings(user_object, name, is_private=True, create_readme=False):
    print("creating repo {}; private:{}; readme:{}".format(name, is_private, create_readme))
    sleep(0.05)
    try:
        repo_object = user_object.get_repo(name)
        print(WARNING_COLOR + "{} exists, skipping create".format(name) + END_COLOR)
    except UnknownObjectException:
        repo_object = user_object.create_repo(name, private=is_private, auto_init=create_readme)
        print("done")

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
