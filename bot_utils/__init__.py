import socket
import requests
import typing
import pika

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


class aiPhilosBotHandler:
    def __init__(self, username, password, host, amqp_port='5762', vhost='/'):
        self.username = username
        self.password = password
        self.host = host
        self.amqp_port = amqp_port
        self.vhost = vhost
        self.connection = None

    def create_channel(self):
        credentials = pika.PlainCredentials(self.username, self.password)

        parameters = pika.ConnectionParameters(self.host,
                                               self.amqp_port,
                                               self.vhost,
                                               credentials)
        self.connection = pika.BlockingConnection(parameters=parameters)
        channel = self.connection.channel()
        channel.basic_qos(prefetch_count=100)
        return channel

    def subscribe(self, channel, to, on_message):
        channel.basic_consume(queue=to, on_message_callback=on_message, auto_ack=False)
        return channel

    def start_consuming(self, channel):
        channel.start_consuming()

    def stop_consuming(self, channel):
        channel.stop_consuming()

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

    def publish(self, channel, target, message, routing_key="*"):
        channel.basic_publish(exchange=target, routing_key=routing_key, body=message.encode())


def get_relevant_keys(input_scheme, relevant_keys):
    keys_found = []
    for key in input_scheme:
        for rel_key in relevant_keys:
            if input_scheme[key] == rel_key:
                keys_found.append(key)
    return keys_found


rechtsformen = [
    "AG",
    "GmbH",
    "KG",
    "OHG",
    "GbR",
    "KGaA",
    "eG",
    "AG & Co. KG",
    "GmbH & Co. KG",
    "Limited & Co. KG",
    "Stiftung & Co. KG",
    "Stiftung GmbH & Co. KG",
    "UG (haftungsbeschränkt) & Co. KG",
    "OHG",
    "GmbH & Co. OHG",
    "AG & Co. OHG",
    "Partenreederei",
    "PartG",
    "PartG mbB",
    "Stille Gesellschaft",
    "gAG",
    "gGmbH",
    "InvAG",
    "KGaA",
    "AG & Co. KGaA",
    "SE & Co. KGaA",
    "GmbH & Co. KGaA",
    "Stiftung & Co. KGaA",
    "REIT-AG",
    "UG (haftungsbeschränkt)",
    "AöR",
    "eG",
    "Eigenbetrieb",
    "Einzelunternehmen",
    "e. V.",
    "KöR",
    "Regiebetrieb",
    "Stiftung",
    "VVaG",
    "SE",
    "SCE",
    "EWIV",
    "Corp.",
    "Corp",
    "Limited",
    "Ltd.",
    "Ltd",
    "LLC",
    "LLP"
]
