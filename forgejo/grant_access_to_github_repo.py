#!/usr/bin/python3

import argparse
from time import sleep
from utils import auth, create_repo_with_settings, change_an_access

GIVE = '-g'
REMOVE = '-r'
PULL = '-p'
TOKEN = '-t'
ADMIN = '-a'
TOKEN_DEST = 'token'
ACTION = 'append'
GIVE_DEST = 'give_access'
REMOVE_DEST = 'remove_access'

def get_args():
    parser = argparse.ArgumentParser(description="Manage Forgejo repository access")
    parser.add_argument(TOKEN, type=str, required=True, dest=TOKEN_DEST, help="Path to token file")
    parser.add_argument(GIVE, action=ACTION, dest=GIVE_DEST, default=[], help="Add access: owner/repo:user1,user2")
    parser.add_argument(REMOVE, action=ACTION, dest=REMOVE_DEST, default=[], help="Remove access: owner/repo:user1,user2")
    parser.add_argument(PULL, action='store_true', help="Grant read-only access")
    parser.add_argument(ADMIN, action='store_true', help="Grant admin access")
    return parser.parse_args()

def process_access_list(session, access_list, give_access, pull=False, admin=False):
    for item in access_list:
        repo_spec, users = item.split(':', 1)
        owner, repo = repo_spec.split('/', 1)
        
        print(f"Processing {owner}/{repo} - {'Add' if give_access else 'Remove'} access")
        
        repo_info = create_repo_with_settings(session, owner, repo)
        if not repo_info:
            continue
        
        change_an_access(session, 
                         users.split(','), 
                         owner, 
                         repo, 
                         give_access, 
                         pull, 
                         admin)

def main():
    args = get_args()
    session = auth(args.token)
    
    if args.give_access:
        process_access_list(session, args.give_access, True, args.p, args.a)
    
    if args.remove_access:
        process_access_list(session, args.remove_access, False)

if __name__ == "__main__":
    main()