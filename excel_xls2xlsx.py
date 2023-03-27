import os
import re
from xls2xlsx import XLS2XLSX
from web_handler.funcs import *
import pyexcel as p


downLoadPath = os.path.join(os.path.expanduser("~"), 'Downloads') + '\\'


def newest(path, suffix=None):
    """
    suffix: suffix for specific file, or default to find newest file but don't care about suffix.
    """
    if suffix:
        files = [i for i in os.listdir(path) if i.__contains__(suffix)]
    else:
        files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


def formatXlsToXLSX():
    # waitWithSec(10)
    newestXLS = newest(downLoadPath)
    newestXLSName = newestXLS.replace(downLoadPath, '').replace('.xls', '')
    x2x = XLS2XLSX(newestXLS)
    x2x.to_xlsx(newestXLSName + '.xlsx')


formatXlsToXLSX()
