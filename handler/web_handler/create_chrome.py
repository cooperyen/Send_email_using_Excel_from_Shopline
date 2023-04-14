import os
from handler.web_handler.setting import port
from handler.web_handler.funcs import *

# cmd setting.


def createChrome(chromePath):
    # print(chromePath)
    # chromePath = 'C:/Users/coope/AppData/Local/Google/Chrome/Application/chrome.exe'
    # chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    chromeUserLoginTemporaryData = 'C:/selenium/AutomationProfile'
    cmdCommand = f'"{chromePath}" --remote-debugging-port={port} --user-data-dir="{chromeUserLoginTemporaryData}"'
    os.popen(cmdCommand)

def pathCheckChrome(chromePath):
    # print(chromePath)
    return os.path.exists(chromePath)

