# coding: utf-8
"""Параллельный запуск нескольких клиентов для kvserver.

Для выполнения параллельных запросов к kvserver используются отдельные процессы.  Их количество
настраивается в переменной CLIENTS.  Работа с процессами реализована с помощью модуля multiprocessing.

Каждый клиент выполняет неколько STORE и GET команд.  Их количество задаётся переменными
STORE_OPERATIONS и GET_OPERATIONS.

Ключи и значения генерируются случайно, на основе заданных алфавита и длины -- переменные KEY_ALPHABET,
VALUE_ALPHABET, KEY_LENGTH, VALUE_LENGTH.
"""


import multiprocessing
import random
import itertools
from datetime import datetime
import time
import logging

import kvclient


# Количество процессов-клиентов
CLIENTS = 2

# Количество операций
STORE_OPERATIONS = 10
GET_OPERATIONS = 10

# Настройка тестовых ключей и значений
KEY_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'
VALUE_ALPHABET = 'abcdefghijklmnopqrstuvwxyz0123456789'
KEY_LENGTH = 10
VALUE_LENGTH = 10


def genkey():
    return ''.join(random.sample(KEY_ALPHABET, KEY_LENGTH))


def genvalue():
    return ''.join(random.sample(VALUE_ALPHABET, VALUE_LENGTH))


def random_keys():
    while True:
        yield genkey()


def run_store_operations():
    data = {genkey(): genvalue() for i in xrange(STORE_OPERATIONS)}
    for key, value in data.iteritems():
        command = kvclient.StoreCommand(key, value)
        command.run()
    return data


def run_get_operations(data):
    infinite_keys = itertools.chain(data.iterkeys(), random_keys())
    test_keys = itertools.islice(infinite_keys, GET_OPERATIONS)
    for key in test_keys:
        command = kvclient.GetCommand(key)
        command.run()

def test():
    data = run_store_operations()
    run_get_operations(data)


def start_test():
    start_time = datetime.now()
    pool = multiprocessing.Pool(CLIENTS)
    pool.apply(test)
    for i in xrange(CLIENTS):
        pool.apply_async(test)
    pool.close()
    pool.join()

    finish_time = datetime.now()
    print '{} STOREs, {} GETs, {} clients'.format(STORE_OPERATIONS, GET_OPERATIONS, CLIENTS)
    print '{}'.format(finish_time - start_time)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    start_test()