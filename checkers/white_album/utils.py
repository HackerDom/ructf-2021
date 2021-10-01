import random
import uuid
import string
from random import randrange

UserAgents = None
Names = None


def get_user_agent():
    global UserAgents
    if UserAgents is None:
        with open('user-agents') as fin:
            UserAgents = [line.strip() for line in fin]
    return random.choice(UserAgents)


def get_album_name():
    return F"album-{str(uuid.uuid4())}"


def get_author_name():
    return f"author-{str(uuid.uuid4())}"


def get_description():
    return f"description-{str(uuid.uuid4())}"


def single_name():
    return f"single-{str(uuid.uuid4())}"


def get_track():
    return f"track-{str(uuid.uuid4())}"