# from xls2xlsx import XLS2XLSX
# name = 'testsss'
# x2x = XLS2XLSX(name+".xls")
# wb = x2x.to_xlsx(name+'.xlsx')


import os

# "C:\Users\coope\Downloads"

desk = os.path.join(os.path.expanduser("~"), 'Downloads') + '\\'
print(desk)


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


a = newest(desk)
b = a.replace(desk, '')

print(b)
