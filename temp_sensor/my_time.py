import utime

PST_OFFSET = -8 * 60 * 60
PDT_OFFSET = -7 * 60 * 60


def local_s():
    return utime.time() + PDT_OFFSET
    # TODO: Automatically handle daylight saving time!
    # is_leap_year = (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0))

def localtime():
    return utime.localtime(local_s())
