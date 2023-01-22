import time
import datetime

start = time.process_time()
end = time.process_time()
time_cost = datetime.timedelta(int(end-start))
print('the time cost is '+str(time_cost))