from account.models import Account
from farm_directory.models import FarmDirectory


def create_test_user(username="test_username", email="testemail@email.com", password="test_password", **kwargs):
    new_user = Account.objects.create_user(username, email, password, **kwargs)
    return new_user


def create_farm_directory_entry(account, **kwargs):
    new_farn_entry = FarmDirectory(account=account, **kwargs)
    new_farn_entry.save()
    return new_farn_entry
