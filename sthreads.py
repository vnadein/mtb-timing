#!/usr/bin/python3.5
from config import *
from threading import Thread


class SystemThreads:
    def __init__(self):
        self.sys_threads = dict()

    def not_exists_or_dead(self, name):
        return name not in self.sys_threads or \
          not self.sys_threads[name].is_alive()

    def start_thread(self, func, name=None):
        name = name or func.__name__
        if self.not_exists_or_dead(name):
            log.info('\n\n '+paint('[sys][threads]', GREEN)+paint(' creating thread ' + str(name), CYAN)+'\n')
            self.sys_threads[name] = Thread(target=func, name=name)
            self.sys_threads[name].start()
        else:
            log.warning('\n\n '+paint('[sys][threads]', GREEN)+paint(' thread ' + str(name) + ' is already running!', CYAN)+'\n')

    def join(self, name):
        th = self.sys_threads.get(name)
        if th:
            th.join()
