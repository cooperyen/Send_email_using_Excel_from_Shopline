
import time
import datetime

a = time.asctime(time.localtime(
    time.time())).replace(' ', '').replace(':', '')

print(f'{str(datetime.date.today())}_one_order'.replace('-', ''))
# 'C:\\Users\\admin\\Desktop\\'
