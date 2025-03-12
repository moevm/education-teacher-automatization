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
from time import sleep

from utils import auth, change_an_access, get_user_object

GIVE = '-g'
REMOVE = '-r'
PULL = '-p'
TOKEN = '-t'
ADMIN = '-a'
TOKEN_DEST = 'token'
TOKEN_HELP = 'path to the text file containing the github token'
ACTION = 'append'
GIVE_DEST = 'give_access'
REMOVE_DEST = 'remove_access'
GIVE_HELP = "add user's accesses to the repo"
REMOVE_HELP = "withdraw user's accesses to the repo"
ADMIN_HELP = "add admin for user's accesses to the repo"
BEGIN_OF_INFO = 13
LEN_OF_HTTPS = 7


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
    parser.add_argument(PULL, type=bool,
                        default=False,
                        help=REMOVE_HELP)
    parser.add_argument(ADMIN, type=bool,
                        default=False,
                        help=ADMIN_HELP)
    results = parser.parse_args()
    return results


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
