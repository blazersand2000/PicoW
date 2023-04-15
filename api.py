import network
import urequests
import time

from machine import Pin

def main():
    wlan = connect()
    while True:
        try:
            log('Fetching weather for Tampa...')
            url = 'https://api.open-meteo.com/v1/forecast?latitude=27.95&longitude=-82.46&hourly=temperature_2m&current_weather=true&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch'
            r = urequests.get(url)
            data = r.json()
            r.close()
            temp = data['current_weather']['temperature']
            log(f'Current temperature in Tampa is {temp} F.')
        except:
            log("could not connect (status =" + str(wlan.status()) + ")")
            log("trying to reconnect...")
            wlan.disconnect()
            wlan = connect()
        time.sleep(60)

def connect():
    ssid = 'Tom Brady - G.O.A.T.'
    password = 'ripcityforever'
    hostname = 'Andrew_PicoW'

    network.hostname(hostname)
    network.country('US')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    wlan.connect(ssid, password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        log('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        log('connected')
        status = wlan.ifconfig()
        log( 'ip = ' + status[0] )
        
    return wlan

def log(s):
    f = lambda n : f'0{n}' if n < 10 else f'{n}'
    t = time.localtime()
    print(f'{t[0]}-{f(t[1])}-{f(t[2])} {f(t[3])}:{f(t[4])}:{f(t[5])}\t{s}')
    

if __name__ == "__main__":
    main()