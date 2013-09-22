# coding: utf-8
"""Демонстрация влияния GIL на многопоточность в CPython.

Скрипт считает время выполнения функции count в один и в два потока.
При запуске на многоядерной машине можно было бы ожидать, что два потока
справятся с задачей в два раза быстрее.  Однако, интерпретатор CPython
даёт обратный результат: однопоточная версия работает примерно на треть
быстрее.

Такой результат связан с тем, что в CPython в каждый момент времени
работает только один поток, выполняющий байт-код Python.  Этот подход
реализован с помощью глобального лока -- Global Interpretator Lock (GIL).

Основано на статье: http://habrahabr.ru/post/84629/
"""


import timeit
from threading import Thread

TEST_RUNS = 1
COUNT_TO = 1000 * 1000 * 100


def count(n):
    while (n > 0):
        n -= 1


def one_thread_test():
    count(COUNT_TO)


def two_threads_test():
    t1 = Thread(target=count, args=(COUNT_TO/2,))
    t1.start()
    t2 = Thread(target=count,args=(COUNT_TO/2,))
    t2.start()
    t1.join(); t2.join()
        

if __name__ == "__main__":
    print 'One-thread run (count to {})'.format(COUNT_TO)
    print timeit.timeit('one_thread_test()', setup="from __main__ import one_thread_test", number=TEST_RUNS)
    print 'Two-threads run (count to {})'.format(COUNT_TO)
    print timeit.timeit('two_threads_test()', setup="from __main__ import two_threads_test", number=TEST_RUNS)
