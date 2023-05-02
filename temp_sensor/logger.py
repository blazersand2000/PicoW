import utime

def log_info(s, shouldPrint = True):
    info = __log(s, shouldPrint)
    return info

def log_warning(s, shouldPrint = True):
    warning = __log(s, shouldPrint)
    return warning

def log_error(s, shouldPrint = True):
    error = __log(s, shouldPrint)
    return error

def __log(s, shouldPrint = True):
    f = lambda n : f'0{n}' if n < 10 else f'{n}'
    t = utime.localtime()
    log = f'{t[0]}-{f(t[1])}-{f(t[2])} {f(t[3])}:{f(t[4])}:{f(t[5])}\t{s}'
    if shouldPrint:
        print(log)
    return log