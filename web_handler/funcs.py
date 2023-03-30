from time import sleep
import random


def wait():
    return sleep(random.randrange(2, 5))


def waitWithSec(sec=1.5):
    return sleep(sec)
