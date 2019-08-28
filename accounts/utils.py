import string
import random


def generate_token(size=25, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))