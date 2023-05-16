ssid = 'Primo Espresso Guest'
password = 'singlelatte'

def url(name, current_temperature):
    return f'https://groker.init.st/api/events?accessKey=ist_h4EB4O8i5-Y6Z2BA3Rp51sMk9LMWYhJ7&bucketKey=4V9V8P4J36AT&{name}={current_temperature}'
