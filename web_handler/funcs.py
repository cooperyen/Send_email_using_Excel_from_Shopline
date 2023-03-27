from time import sleep
import random


def wait():
    return sleep(random.randrange(2, 5))


def waitWithSec(sec):
    return sleep(sec)
