# coding: utf-8
import sys
import socket
import logging

from socket_utils import receive_all, send_all


def create_connection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8001))
    return s


def send_command(clientsocket, command):
    send_all(clientsocket, command)


def receive_answer(clientsocket):
    return receive_all(clientsocket)


class StoreCommand(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def run(self):
        logging.info('executing store command (key: {}, value: {})'.format(self.key, self.value))
        clientsocket = create_connection()
        command = ' '.join(('store', self.key, self.value))
        send_command(clientsocket, command)
        logging.info('command was sent')
        clientsocket.shutdown(socket.SHUT_RDWR)
        clientsocket.close()
        return True


class GetCommand(object):
    def __init__(self, key):
        self.key = key

    def run(self):
        logging.info('executing get command (key: {})'.format(self.key))
        clientsocket = create_connection()
        command = ' '.join(('get', self.key))
        send_command(clientsocket, command)
        logging.info('command was sent')
        clientsocket.shutdown(socket.SHUT_WR)

        value = receive_answer(clientsocket)
        logging.info('answer: {}'.format(value))
        clientsocket.shutdown(socket.SHUT_RD)
        clientsocket.close()
        print 'value: {}'.format(value)
        return True


def parse_command(command):
    chunks = command.split(' ')
    if chunks[0] == 'store':
        key = chunks[1].strip()
        value = chunks[2].strip()
        return StoreCommand(key, value)
    elif chunks[0] == 'get':
        key = chunks[1].strip()
        return GetCommand(key)
    else:
        return None


def read_command():
    command = sys.stdin.readline()
    return parse_command(command)


def execute_command():
    command = read_command()
    if command:
        return command.run()
    else:
        print 'unknown command'
        return True


def start_client():
    should_continue = execute_command()
    while should_continue:
        should_continue = execute_command()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    start_client()
