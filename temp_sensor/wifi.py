import network
import uasyncio
import queue
from logger import log

wifi_statuses = {-3: 'Incorrect password', -2: 'No matching SSID found', -1: 'Connection failed',
                    0: 'Link is down', 1: 'Connecting', 2: 'No IP address', 3: 'Successfully connected'}

async def wifi_loop(q: queue.Queue):
    ssid = 'Tom Brady - G.O.A.T.'
    password = 'ripcityforever'
    hostname = 'Andrew_PicoW'
    connected = False
    status = 'Connecting'
    ip = ''

    await q.put({'connected': connected, 'status': status, 'ip': ip})

    wlan = None
    while True:
        print(wlan)
        if wlan is None or wlan.status() != 3:
            if wlan is not None:
                wlan.disconnect()
            wlan = await connect(ssid, password, hostname)
        new_status = get_status_text(wlan.status())
        new_ip = '' if wlan.status() != 3 else wlan.ifconfig()[0]                 
        if status != new_status or ip != new_ip:
            # send queue message with new values
            connected = wlan.status() == 3
            status = new_status
            ip = new_ip
            await q.put({'connected': connected, 'status': status, 'ip': ip})
        log_info('sleeping 1')
        await uasyncio.sleep(1)

async def connect(ssid, password, hostname):
    network.hostname(hostname)
    network.country('US')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm=0xa11140)  # Disable power-save mode
    wlan.connect(ssid, password)

    max_wait = 10
    while max_wait > 0:
        """
            0   STAT_IDLE -- no connection and no activity,
            1   STAT_CONNECTING -- connecting in progress,
            2   Connected to wifi, but no IP address
            -3  STAT_WRONG_PASSWORD -- failed due to incorrect password,
            -2  STAT_NO_AP_FOUND -- failed because no access point replied,
            -1  STAT_CONNECT_FAIL -- failed due to other problems,
            3   STAT_GOT_IP -- connection successful.
        """
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        log_info('waiting for connection...')
        await uasyncio.sleep(1)

    status_code = wlan.status()
    status_text = get_status_text(status_code)
    if status_code != 3:
        log_info(f'WiFi error: {status_text}. Retrying...')
        #raise RuntimeError('network connection failed')
    else:
        status = wlan.ifconfig()
        log_info(f'Connected to WiFi; IP: {status[0]}')
        # log_info('ip = ' + status[0])

    return wlan

def get_status_text(status_code):
    return wifi_statuses.get(status_code) if status_code in wifi_statuses.keys() else wifi_statuses[-1]