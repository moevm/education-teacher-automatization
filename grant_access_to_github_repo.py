#!/usr/bin/python3
# Script is able to give/withdraw an access to repo's to the users
# For getting token go to https://github.com/settings/tokens
# Use "" for example
# ./give_repo_access.py -t "dabae5f9ae72384880286fcda352f682b5a38004"
# Repolink is a string of following format:
# <user>/<repo>
# <org>/<repo>
# Give an access:
# ./give_repo_access.py -g=repolink:user1,user2,user3 -g=repolink:user12,user12,user33 -t "token"
# remove an access:
# ./give_repo_access.py -r=repolink:user1,user2,user3 -r=repolink:user12,user12,user33 -t "token"
# Give and remove an access:
# ./give_repo_access.py -r=repolink:user2,user3 -g=repolink:user12 -t "token"
# Give an reading access:
# ./give_repo_access.py -g=repolink:user12 -p True -t "token"


import argparse
import github
from github.GithubException import UnknownObjectException
from time import sleep

GIVE = '-g'
REMOVE = '-r'
PULL = '-p'
TOKEN = '-t'
ADMIN = '-a'
TOKEN_DEST = 'token'
TOKEN_HELP = 'take your token from github account'
ACTION = 'append'
GIVE_DEST = 'give_access'
REMOVE_DEST = 'remove_access'
GIVE_HELP = "add user's accesses to the repo"
REMOVE_HELP = "withdraw user's accesses to the repo"
ADMIN_HELP = "add admin for user's accesses to the repo"
BEGIN_OF_INFO = 13
LEN_OF_HTTPS = 7
FAIL_COLOR = '\033[91m'
WARNING_COLOR = '\033[33m'
END_COLOR = '\033[0m'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(TOKEN, type=str, required=True,
                        dest=TOKEN_DEST,
                        help=TOKEN_HELP)
    parser.add_argument(GIVE, action=ACTION,
                        dest=GIVE_DEST, default=[],
                        help=GIVE_HELP)
    parser.add_argument(REMOVE, action=ACTION,
                        dest=REMOVE_DEST, default=[],
                        help=REMOVE_HELP)
    parser.add_argument(PULL,
                        default=False,
                        help=REMOVE_HELP)
    parser.add_argument(ADMIN,
                        default=False,
                        help=ADMIN_HELP)
    results = parser.parse_args()
    return results


def give_an_access(collaborator, user_object, repo, pull=False, admin=False):
    print("adding {} to collaborators ...".format(collaborator))
    sleep(0.05)
    try:
        repo_object = user_object.get_repo(repo)
        print("{} exists".format(repo))
    except UnknownObjectException:
        print("{} does not exist, creating".format(repo))
        repo_object = user_object.create_repo(repo)
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


def remove_an_access(collaborator, user_object, repo):
    print("remove {} from collaborators ...".format(collaborator))
    try:
        user_object.get_repo(repo).remove_from_collaborators(collaborator)
    except:
        print("Collaborator {} does not exist or waits for invite".format(collaborator))


def change_an_access(users, user_object, repo, give, pull=False, admin=False):
    for user in users:
        if give:
            give_an_access(user, user_object, repo, pull, admin)
        else:
            remove_an_access(user, user_object, repo)


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
    except:
        print("Authorization failed")
        exit()


def processing_access_list(github_object, access_list, giving, pull=False, admin=False):
    for obj in access_list:
        sleep(0.05)
        repo_link, users = obj.split(':')
        print(repo_link, pull)
        repo_owner, repo = repo_link.split('/')
        print('Owner: {}, repo: {}'.format(repo_owner, repo))
        user_object = get_user_object(github_object, repo_owner)
        sleep(0.05)
        change_an_access(users.split(','), user_object, repo, giving, pull, admin)


def main():
    args = get_args()
    github_object = auth(args.token)
    give_an_access_list, remove_an_access_list, pull = args.give_access, args.remove_access, args.p
    admin = args.a
    processing_access_list(github_object, give_an_access_list, True, pull, admin)
    processing_access_list(github_object, remove_an_access_list, False)


if __name__ == "__main__":
    main()
