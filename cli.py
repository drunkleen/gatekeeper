import os
import django
from getpass import getpass
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GateKeeper.settings")
django.setup()

from core.models import UserAccount


def create_admin_user():
    while True:
        username = input('Enter username: ')
        if username is not None and len(username) > 3:
            break
        print("username is not acceptable! please try again.")

    while True:
        email = input('Enter email: ')
        if email is not None and "@" in email and "." in email and len(email) > 9:
            break
        print("Email are not acceptable! please try again.")

    while True:
        password = getpass('Enter password: ')
        repeated_password = getpass('Repeat password: ')
        if password == repeated_password:
            break
        print("Passwords does not match! please try again.")
    try:
        admin_user = UserAccount.objects.create_user(
            username=username,
            email=email,
            account_type=UserAccount.type_admin,
        )

        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password(password)
        admin_user.save()
    except Exception as e:
        print(f"an error occurred while creating\n{e}")

    print(f"Admin user '{username}' created successfully.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "createadmin":
        create_admin_user()
