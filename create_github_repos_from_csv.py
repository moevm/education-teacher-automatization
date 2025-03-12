#!/usr/bin/python3

import argparse
import csv

from grant_access_to_github_repo import get_user_object, auth, TOKEN, TOKEN_DEST, TOKEN_HELP
from utils import give_an_access, create_repo_with_settings, print_fail

FILE = '-f'
FILE_DEST = 'file'
FILE_HELP = 'path to the csv table with input data'
TEMPLATE = '--template'
TEMPLATE_DEST = 'template'
BRANCH_PROTECTION = '--branch_protection'
BRANCH_PROTECTION_DEST = 'branch_protection'

class RepoConfig:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.is_private = kwargs.get('is_private')
        self.create_readme = kwargs.get('create_readme')
        self.create_from_template = kwargs.get('template')
        self.branch_protection = kwargs.get('branch_protection')
        self.read_login_list = kwargs.get('read_login_list') if kwargs.get('read_login_list') != [''] else []
        self.write_login_list = kwargs.get('write_login_list') if kwargs.get('write_login_list') != [''] else []
        self.admin_login_list = kwargs.get('admin_login_list') if kwargs.get('admin_login_list') != [''] else []

    def __str__(self):
        to_return = ("name: {}\nis_private: {}\ncreate_readme: {}\nread_login_list: {} \nwrite_login_list: {"
                     "}\nadmin_login_list: {}")
        return to_return.format(self.name, self.is_private, self.create_readme,
                                self.read_login_list, self.write_login_list,
                                self.admin_login_list)


def split_logins(logins_str, delimiter=','):
    return [login.lower() for login in logins_str.split(delimiter)]


def check_file_name(filename):
    return filename.endswith(".csv")


def read_table(filename, template=False, branch_protection=False):
    answer = []
    if not check_file_name(filename):
        print_fail("incorrect file extension. stop")
        exit(1)
    try:
        with open(filename, newline='') as file:
            rows = csv.reader(file, delimiter=';')
            for row in rows:
                name = row[0]
                is_private = True if row[1].lower() in ['true', '1'] else False
                create_readme = True if row[2].lower() in ['true', '1'] else False
                read_login_list = split_logins(row[3])
                write_login_list = split_logins(row[4])
                admin_login_list = split_logins(row[5])
                answer.append(RepoConfig(name=name, is_private=is_private, create_readme=create_readme,
                                         read_login_list=read_login_list, write_login_list=write_login_list,
                                         admin_login_list=admin_login_list, template=template,
                                         branch_protection=branch_protection))
    except Exception as error:
        print_fail("error work with table: {}. stop".format(error))
        exit(1)

    return answer


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(TOKEN, type=str, required=True,
                        dest=TOKEN_DEST,
                        help=TOKEN_HELP)
    parser.add_argument(FILE, type=str, required=True,
                        dest=FILE_DEST,
                        help=FILE_HELP)
    parser.add_argument(TEMPLATE, type=str, required=False,
                        default=False,
                        dest=TEMPLATE_DEST,
                        help=TEMPLATE_DEST)
    parser.add_argument(BRANCH_PROTECTION, type=str, required=False,
                        default=False,
                        dest=BRANCH_PROTECTION_DEST,
                        help=BRANCH_PROTECTION)
    results = parser.parse_args()

    return results


def process_table(github_object, repo_config):
    users = set()
    invitations = set()
    for config in repo_config:
        repo_owner, repo_name = config.name.split('/')
        user_object = get_user_object(github_object, repo_owner)
        repo_object = create_repo_with_settings(user_object, repo_name, is_private=config.is_private,
                                                create_readme=config.create_readme,
                                                template=config.create_from_template, github_object=github_object,
                                                branch_protection=config.branch_protection)

        if not repo_object:
            continue

        invitations.add("https://github.com/{}/invitations".format(repo_object.full_name))

        for user in config.read_login_list:
            if give_an_access(repo_object, user, pull=True):
                users.add(user)

        for user in config.write_login_list:
            if give_an_access(repo_object, user):
                users.add(user)

        for user in config.admin_login_list:
            if give_an_access(repo_object, user, admin=True):
                users.add(user)

        print()

    print(f"added users: {'; '.join(users)}")
    print("invitations: {}".format('\n'.join(invitations)))


def main():
    args = get_args()
    github_object = auth(args.token)
    table = read_table(args.file, args.template, args.branch_protection)
    process_table(github_object, table)


if __name__ == "__main__":
    main()
