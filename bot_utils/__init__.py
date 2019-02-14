import socket
import requests
import typing
name = "bot_utils"


class Logger:
    """ Sends messages to the logging rest api """

    def __init__(self, bot_id: str, host: str, port: str):
        self.bot_id = bot_id
        self.host = host
        self.port = port
        self.error = 'error'
        self.info = 'info'

    def log_error(self, error: typing.TypeVar):
        """ Log an Error Message """
        message = 'an error occured: ' + str(error)
        self._log(message, self.error)

    def log_info(self, message: typing.TypeVar):
        self._log(message, self.info)

    def _log(self, message, log_type):
        payload = {
            'bot_id': self.bot_id,
            'message': str(message)
        }
        requests.post('http://' + str(self.host) + ':' + str(self.port) + '/logger/' + log_type, json=payload)


class ConnectivityChecker:
    """ Checks availability of a given host. reports error via provided error reporting function """

    def __init__(self, error_reporter: typing.Callable[[str], typing.NoReturn]):
        self.error_reporter = error_reporter

    def is_available(self, host: str, port: int) -> bool:
        server_socket = None
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_result = server_socket.connect_ex((host, port))
            if server_result == 0:
                return True
            else:
                return False
        except (socket.gaierror, socket.herror, socket.error) as err:
            self.error_reporter('error checking for server availability :: ' + str(err))
        finally:
            if server_socket is not None:
                server_socket.close()
