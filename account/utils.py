import requests


def verify_nin(nin) -> tuple:
    """
    Verifies a nin number.
    :returns: tuple.
    """
    verification = requests.post("").json()
    if verification:
        return True, False
    else:
        return False, None


def verify_bvn_number(bvn: str):
    """
    Verifies a bvn number
    """

    verification = requests.post("").json()
    if verification:
        return True, False
    else:
        return False, None
