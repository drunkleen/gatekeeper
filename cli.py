import os
import django
from getpass import getpass
import sys
from rich.console import Console
from rich.table import Table

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GateKeeper.settings")
django.setup()

from core.models import UserAccount
from GateKeeper.settings import DEFAULT_USER_PASSWORD



HELP = [
    ["/q", "quit", "Exit GateKeeper shell"],
    ["/h", "help", "Get help"],
    ["/va", "admin view", "Show admin list"],
    ["/ca", "admin create", "Create new admin account"],
    ["/vm", "mod view", "Show moderator list"],
    ["/cm", "mod create", "Create new moderator account"],
    ["/vu", "user view", "Show user list"],
    ["/cu", "user create", "Create new user account"],
    ["/rmid", "del account id [ID]", "Remove account by id"],
    ["/rmu", "del account username [Username]", "Remove account by username"],
]

class UserManagement:
    def __init__(self) -> None:
        self.console = Console()
        
        
    def get_input(self, field_name: str, message: str, min_input_len: int):
        while True:
            user_input = input(message)
            if user_input is not None and len(user_input) >= min_input_len:
                break
            print(f"{field_name} is not acceptable! please try again.")
        return user_input


    def get_password(self):
        while True:
            password = getpass("Enter password: ")
            repeated_password = getpass("Repeat password: ")
            if password == repeated_password:
                break
            print("Passwords does not match! please try again.")
        return password


    def create_account(self, user_type):
        username = self.get_input("Username", "Enter username: ", 4)
        email = self.get_input("Email", "Enter email: ", 8)
        first_name = self.get_input("First Name", "Enter First Name: ", 3)
        last_name = self.get_input("Enter Last Name", "Enter Last Name: ", 0)
        if user_type != UserAccount.type_user:
            password = self.get_password()
        else:
            password = DEFAULT_USER_PASSWORD

        try:
            admin_user = UserAccount.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                account_type=user_type,
            )

            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.set_password(password)
            admin_user.save()
        except Exception as e:
            print(f"an error occurred while creating the account\n{e}")

        print(f"{user_type} user '{username}' created successfully.")


    def delete_account_by_id(self, account_id):
        try:
            account = UserAccount.objects.get(id=account_id)
            if not account:
                self.console.print("Account not found!", style="bright_orange")
            else:
                self.print_user_list("Selected account", [account])
                self.console.print("Are you sure you want to delete this account? (Y/N)", style="bright_yellow", end="")
                user_choice = input()
                if user_choice.lower() == "y" or user_choice.lower() == "yes":
                    account.delete()
                    self.console.print("Account has been deleted.", style="bright_green")
                
        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:
            print(f"an error occurred while creating the account\n{e}")


    def delete_account_by_username(self, account_username):
        try:
            account = UserAccount.objects.get(username=account_username)
            if not account:
                self.console.print("Account not found!", style="bright_orange")
            else:
                self.print_user_list("Selected account", [account])
                self.console.print("Are you sure you want to delete this account? (Y/N)", style="bright_yellow", end="")
                user_choice = input()
                if user_choice.lower() == "y" or user_choice.lower() == "yes":
                    account.delete()
                    self.console.print("Account has been deleted.", style="bright_green")
                
        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:
            print(f"an error occurred while creating the account\n{e}")


    def create_admin(self):
        self.create_account(UserAccount.type_admin)
        

    def create_moderator(self):
        self.create_account(UserAccount.type_moderator)
        

    def create_user(self):
        self.create_account(UserAccount.type_user)


    def get_all_admins(self):
        try:
            admins = UserAccount.objects.all().filter(account_type=UserAccount.type_admin).order_by("id")
            self.print_user_list("Admin List", admins)
            
        except Exception as e:
            print(f"an error occurred while doing the task\n{e}")


    def get_all_mods(self):
        try:
            mods = UserAccount.objects.all().filter(account_type=UserAccount.type_moderator).order_by("id")
            self.print_user_list("Moderator List", mods)
            
        except Exception as e:
            print(f"an error occurred while doing the task\n{e}")


    def get_all_users(self):
        try:
            users = UserAccount.objects.all().filter(account_type=UserAccount.type_user).order_by("id")
            self.print_user_list("User List", users)
            
        except Exception as e:
            print(f"an error occurred while doing the task\n{e}")


    def print_user_list(self,title:str, query:list):
        table = Table(title=title)
        columns = ["ID", "Usernamee", "First Name", "Last Name", "Email", "Type", "Status"]
        for column in columns:
            table.add_column(column)

        for row in query:
            if row.is_active:
                table.add_row(str(row.id), 
                            row.username, 
                            row.first_name,
                            row.last_name,
                            row.email,
                            row.type_admin,
                            'Active',
                            style='bright_green')
            else:
                table.add_row(str(row.id), 
                            row.username, 
                            row.first_name,
                            row.last_name,
                            row.email,
                            row.type_admin,
                            'Inactive',
                            style='bright_yellow')

        
        self.console.print(table)



# Edeko


class Shell:
    def __init__(self) -> None:
        self.userManagement = UserManagement()
        self.console = Console()
    
    def start_shell(self):
        try:
            while True:
                self.console.print("GareKeeper:~$ ", style='bright_green', end="")
                user_input = input()
                
                if user_input in ("/q", "quit"):
                    sys.exit()
                    
                elif user_input in ("/va", "admin view"):
                    self.userManagement.get_all_admins()
                    
                elif user_input in ("/va", "admin create"):
                    self.userManagement.create_admin()
                        
                elif user_input in ("/vm", "mod view"):
                    self.userManagement.get_all_mods()
                    
                elif user_input in ("/cm", "mod create"):
                    self.userManagement.create_moderator()
                        
                elif user_input in ("/vu", "user view"):
                    self.userManagement.get_all_users()
                    
                elif user_input in ("/cu", "user create"):
                    self.userManagement.create_user()
                    
                elif "/rmid" in user_input or "del account id" in user_input:
                    self.userManagement.delete_account_by_id(int(user_input.split(" ")[-1]))
                    
                elif "/rmu" in user_input or "del account username" in user_input:
                    self.userManagement.delete_account_by_username(user_input.split(" ")[-1])
                
                else:
                    table = Table(title="Need help?")
                    columns = ["short", "Command options", "Action"]
                    for column in columns:
                        table.add_column(column)

                    for row in HELP:
                        table.add_row(*row)
                    self.console.print(table)
        except KeyboardInterrupt:
            sys.exit()
        

if __name__ == "__main__":
    
    
    if len(sys.argv) > 1 and sys.argv[1] == "createadmin":
        userManagement = UserManagement()
        userManagement.create_admin()

    elif len(sys.argv) > 1 and sys.argv[1] == "shell":
        shell = Shell()
        shell.start_shell()
        

