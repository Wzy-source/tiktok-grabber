import time


# 时间处理工具


# 将时间戳转换为YYYY-MM-DD hh:mm:ss格式
def stamp2time(stamp):
    timeArray = time.localtime(stamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeArray)


# 将YYYY-MM-DD hh:mm:ss格式转换为时间戳
def time2stamp(time_str):
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray))


def is_between(begin_time, end_time, cur_stamp):
    begin_stamp = time2stamp(begin_time) if begin_time else 0
    end_stamp = time2stamp(end_time) if end_time else time.time()
    return begin_stamp < cur_stamp < end_stamp
