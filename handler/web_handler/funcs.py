from time import sleep
import random


def wait():
    return sleep(random.randrange(2, 4))


def waitWithSec(sec=1):
    return sleep(sec)
