from logger import log_info
from phew import server
from phew.template import render_template
from state import State
from settings import Settings
from phew.logging import log_file
from lock import lock
import gc

TEMPLATE_PATH = 'templates'

index_template_path = f'{TEMPLATE_PATH}/index.html'


@server.route('/', methods=['GET'])
async def __get(request):
    settings = await State.get_settings()
    return render_template(index_template_path, settings=settings, errors=[], success=''), 200


@server.route('/', methods=['POST'])
async def __post(request):
    settings, errors = __parse_and_validate_settings(request.form)
    if len(errors) > 0:
        settings = await State.get_settings()
        return render_template(index_template_path, settings=settings, errors=errors, success=''), 422
    await State.state_q.put((State.set_settings, settings))
    success = 'Settings saved successfully'
    return render_template(index_template_path, settings=settings, errors=errors, success=success), 200


@server.route('/logs', methods=['GET'])
async def __get(request):
    return render_template(log_file), 200


@server.catchall()
async def __catchall(request):
    return 'Not found!', 404


def __parse_and_validate_settings(form):
    def is_valid_hour(hour):
        return is_int(hour) and int(hour) in range(24)

    def is_valid_minute(minute):
        return is_int(minute) and int(minute) in range(60)

    def is_int(s):
        try:
            int(s)
        except ValueError:
            return False
        return True

    def is_float(s):
        try:
            float(s)
        except ValueError:
            return False
        return True

    def is_valid_brightness(brightness):
        return is_int(brightness) and int(brightness) in range(11)

    def is_valid_temperature(temperature):
        return is_float(temperature)

    def is_valid_temperature_range(min_temp, max_temp):
        if not is_valid_temperature(min_temp) or not is_valid_temperature(max_temp):
            return False
        return float(min_temp) <= float(max_temp)

    hostname = form.get('name', '')
    temp_publish_interval_seconds = form.get('temp-publish-interval', '0')
    min_temp = form.get('min-temp', '0')
    max_temp = form.get('max-temp', '0')
    screen_on_time_of_day_hour = form.get('screen-on-hour', '0')
    screen_on_time_of_day_minute = form.get('screen-on-minute', '0')
    screen_off_time_of_day_hour = form.get('screen-off-hour', '0')
    screen_off_time_of_day_minute = form.get('screen-off-minute', '0')
    brightness = form.get('brightness', '0')
    rotated = form.get('rotated-checkbox', '0')

    errors = []
    if len(hostname) < 1:
        errors.append('Device Name must not be empty')
    temp_publish_intervals = ['30', '60', '300', '600', '1200',
                              '1800', '3600', '7200', '14400', '28800', '43200', '86400']
    if temp_publish_interval_seconds not in temp_publish_intervals:
        errors.append('Invalid Temperature Publish Interval')
    if not is_valid_temperature_range(min_temp, max_temp):
        errors.append('Invalid Temperature Range')
    if not is_valid_hour(screen_on_time_of_day_hour) or not is_valid_minute(screen_on_time_of_day_minute):
        errors.append('Invalid Screen On time')
    if not is_valid_hour(screen_off_time_of_day_hour) or not is_valid_minute(screen_off_time_of_day_minute):
        errors.append('Invalid Screen Off time')
    if not is_valid_brightness(brightness):
        errors.append('Invalid Screen Brightness')
    if len(errors) > 0:
        return None, errors
    settingsDict = {
        "hostname": hostname,
        "tempPublishIntervalSeconds": int(temp_publish_interval_seconds),
        "minTemp": float(min_temp),
        "maxTemp": float(max_temp),
        "screenOnTimeOfDay": {"hour": int(screen_on_time_of_day_hour), "minute": int(screen_on_time_of_day_minute)},
        "screenOffTimeOfDay": {"hour": int(screen_off_time_of_day_hour), "minute": int(screen_off_time_of_day_minute)},
        "brightness": int(brightness) / 10,
        "rotated": rotated.lower() == "true"
    }
    return Settings(settingsDict), errors


def __get_logs():
    with lock:
        with open(log_file, 'r') as file:
            yield from file


def run():
    server.run()
