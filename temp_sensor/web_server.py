from logger import log_info
from phew import server

TEMPLATE_PATH = "templates"

@server.route("/", methods=["GET"])
def __get(request):
    return "I got it!", 200


@server.route("/", methods=["POST"])
def __post(request):
    return "I got it!", 200


@server.catchall()
def __catchall(request):
    return "Not found!", 404


def run():
    server.run()
