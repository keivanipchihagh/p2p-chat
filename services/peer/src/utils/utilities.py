import string
import random


def generate_random_string(length: int) -> str:
    """
        Generate a random string of given length.
    """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_port() -> str:
    """
        Generate a random port.
    """
    return random.choice(range(1000, 8000))