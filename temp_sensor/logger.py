import time

def log(s, shouldPrint = True):
    f = lambda n : f'0{n}' if n < 10 else f'{n}'
    t = time.localtime()
    log = f'{t[0]}-{f(t[1])}-{f(t[2])} {f(t[3])}:{f(t[4])}:{f(t[5])}\t{s}'
    if shouldPrint:
        print(log)
    return log