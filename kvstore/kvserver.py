import socket
import logging
import traceback

from socket_utils import receive_all, send_all


class StoreCommand(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def run(self, storage, clientsocket):
        storage[self.key] = self.value


class GetCommand(object):
    def __init__(self, key):
        self.key = key

    def run(self, storage, clientsocket):
        val = storage.get(self.key)
        if val is not None:
            write_answer(clientsocket, val)


def parse_command(command):
    chunks = command.split(' ')
    if chunks[0] == 'store':
        key = chunks[1]
        value = chunks[2]
        return StoreCommand(key, value)
    elif chunks[0] == 'get':
        key = chunks[1]
        return GetCommand(key)
    else:
        return None


def write_answer(clientsocket, answer):
    logging.info('answer: {}'.format(answer))
    send_all(clientsocket, answer)
    logging.info('answer was sent')
    clientsocket.shutdown(socket.SHUT_WR)


def receive_command(clientsocket):
    c = receive_all(clientsocket)
    logging.info('raw command: {}'.format(c))
    return parse_command(c)


def process_client(clientsocket, storage):
    logging.info('new client')
    command = receive_command(clientsocket)
    command.run(storage, clientsocket)
    clientsocket.close()
    logging.info('client processed')


def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8001))
    server_socket.listen(5)
    logging.info('server socket created')
    return server_socket


def start_server():
    storage = dict()
    serversocket = create_server_socket()

    while 1:
        (clientsocket, address) = serversocket.accept()
        try:
            process_client(clientsocket, storage)
        except Exception as e:
            logging.error('error!\n{}'.format(traceback.format_exc()))
            clientsocket.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_server()
