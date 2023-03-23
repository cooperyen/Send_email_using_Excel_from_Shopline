import funcs


# print(funcs.wait)


def elementTarget(driver, dom, way):
    funcs.wait()
    return driver.find_element(
        way, dom)
