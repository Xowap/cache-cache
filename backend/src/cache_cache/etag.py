import random
import re
import string
import tempfile


def get_etag_file_path():
    """Get the file path of etag file in a temporary directory"""

    return tempfile.gettempdir() + "/etag.txt"


def generate_random_string(length=20):
    """Still not sure why this function isn't part of the standard lib yet"""

    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def get_etag():
    """Retrieve the etag from the etag.txt file."""

    etag_file = get_etag_file_path()

    try:
        with open(etag_file, "r") as file:
            etag = file.read()
    except FileNotFoundError:
        etag = None

    return etag


def set_etag(etag):
    """Set the etag in the etag.txt file."""

    etag_file = get_etag_file_path()

    with open(etag_file, "w") as file:
        file.write(etag)


def get_or_set_etag():
    """For demonstration purposes we store the etag in the etag.txt file."""

    etag = get_etag()

    if etag is None:
        etag = generate_random_string()
        set_etag(etag)

    return etag


def extract_etag(inm: str) -> str:
    """Uncorks the ETag which should be received quoted from the request"""

    if m := re.match(r'^(W/)?"(?P<etag>.*)"$', inm):
        return m.group("etag")
    else:
        return inm
