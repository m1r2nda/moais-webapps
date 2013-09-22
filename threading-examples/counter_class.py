import threading


COUNT_TO = 100


class Counter(object):
    def __init__(self, count_to):
        self.__counter = count_to

    def count(self):
        self.__counter -= 1;

    def get_value(self):
        return self.__counter


class CounterThread(threading.Thread):
    def __init__(self, counter, count_lock, name):
        super(CounterThread, self).__init__(name=name)
        self.__counter = counter
        self.__count_lock = count_lock

    def run(self):
        while True:
            with self.__count_lock:
              v = self.__counter.get_value()
              if (v <= 0):
                  break
              print '{} (thread {})'.format(v, threading.current_thread().name)
              self.__counter.count()


def start_count(count_to):
    counter = Counter(count_to)
    count_lock = threading.Lock()
    t1 = CounterThread(counter, count_lock, name='1')
    t2 = CounterThread(counter, count_lock, name='2')
    t1.start()
    t2.start()
    t1.join()
    t2.join()


if __name__ == "__main__":
    start_count(COUNT_TO)              

