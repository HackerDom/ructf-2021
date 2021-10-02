import random
import string

from request_pb2 import NewEmployee, FullName, BankCard, Location

ALPHA = string.ascii_lowercase + string.digits


def gen_string(a=20, b=20):
    return ''.join(random.choice(ALPHA) for _ in range(random.randint(a, b)))


def gen_description():
    return ' '.join([gen_string(10, 20) for _ in range(1, 4)])


def gen_employee(flag):
    name = FullName(
        firstName=gen_string(4, 6),
        secondName=gen_string(4, 6),
        middleName=gen_string(4, 6),
    )
    card = BankCard(
        number=flag,
        cardholder=gen_string(),
        cvv=str(random.randint(0, 999)).zfill(3),
    )
    location = Location(
        country=gen_string(),
        city=gen_string(),
    )
    return NewEmployee(
        name=name,
        card=card,
        location=location,
        description=gen_description(),
        tags=["new_employee", gen_string(), gen_string()],
    )
