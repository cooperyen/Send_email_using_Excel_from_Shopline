from handler.web_handler.funcs import *


# print(funcs.wait)


def elementTarget(driver, dom, way):
    wait()
    return driver.find_element(
        way, dom)
