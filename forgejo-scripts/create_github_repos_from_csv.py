import argparse
import csv

from utils import auth, create_repo_with_settings, give_an_access, print_fail, FORGEJO_HOST

TOKEN = '-t'
TOKEN_DEST = 'token'
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
        self.template = kwargs.get('template')
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

class ForgejoError(Exception):
    pass

def split_logins(logins_str, delimiter=','):
    return [login.lower() for login in logins_str.split(delimiter)]

def check_file_name(filename):
    return filename.endswith(".csv")

def read_table(filename, template=False, branch_protection=False):
    answer = []
    if not check_file_name(filename):
        raise ForgejoError("Incorrect file extension. Expected .csv")
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
    except FileNotFoundError:
        raise ForgejoError(f"File not found: {filename}")
    except Exception as e:
        raise ForgejoError(f"Error reading table: {e}")

    return answer

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(TOKEN, dest=TOKEN_DEST, type=str, required=True, help="Path to token file")
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

def process_table(session, repo_config):
    users = set()
    invitations = set()
    for config in repo_config:
        repo_owner, repo_name = config.name.split('/')
        repo_object = create_repo_with_settings(session, repo_owner, repo_name, config.is_private, config.create_readme, config.template, config.branch_protection)

        if not repo_object:
            continue

        invitations.add("https://{}/{}/{}/invitations".format(FORGEJO_HOST, repo_owner, repo_name))

        for user in config.read_login_list:
            if give_an_access(session, repo_owner, repo_name, user, permission='read'):
                users.add(user)

        for user in config.write_login_list:
            if give_an_access(session, repo_owner, repo_name, user, permission='write'):
                users.add(user)

        for user in config.admin_login_list:
            if give_an_access(session, repo_owner, repo_name, user, permission='admin'):
                users.add(user)

        print()

    print(f"added users: {'; '.join(users)}")
    print("invitations: {}".format('\n'.join(invitations)))

def main():
    args = get_args()
    session = auth(args.token)
    table = read_table(args.file, args.template, args.branch_protection)
    process_table(session, table)

if __name__ == "__main__":
    main()
