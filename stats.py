import random
from math import log


def duration_distribution():
    return random.random() * 6


def successive_call_distribution():
    return -log(random.random()) * 6


def make_successive_call_distribution(mean):

    def f():
        return -log(random.random()) * mean

    return f
