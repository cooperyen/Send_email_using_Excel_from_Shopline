import os
from web_handler.setting import port
from web_handler.funcs import *

# cmd setting.


def createChrome(chromePath):
    # print(chromePath)
    # chromePath = 'C:/Users/coope/AppData/Local/Google/Chrome/Application/chrome.exe'
    # chromePath = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
    chromeUserLoginTemporaryData = 'C:/selenium/AutomationProfile'
    cmdCommand = f'"{chromePath}" --remote-debugging-port={port} --user-data-dir="{chromeUserLoginTemporaryData}"'

    print(os.path.exists(chromePath))
    # os.popen(cmdCommand)
    
    # wait()

def pathCheckChrome(chromePath):
    return os.path.exists(chromePath)


