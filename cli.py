import os
import django
from getpass import getpass

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GateKeeper.settings")
django.setup()

from core.models import UserAccount


def create_admin_user():
    username = input('Enter username: ')
    email = input('Enter email: ')
    while True:
        password = getpass('Enter password: ')
        repeated_password = getpass('Repeat password: ')
        if password == repeated_password:
            break
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
    create_admin_user()
