"""
Test data that can be used for examining the website. Not exactly a "test" per 
say, but provides a lot of useful premade users that can be examined for quick
examination of how a useful preset collection of users interacts with the web-
site.
"""
from app.app import create_app
from app.models import User


def create_users():
    """
    Populates the app database with a collection of users.
    """
    # Create a user that has a populated table of reputation.
    #profile_user = User()


def main():
    app = create_app()
    create_users()


if __name__ == '__main__':
    main()
