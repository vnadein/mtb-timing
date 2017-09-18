#!/usr/bin/python3.5
from config import *
from sthreads import SystemThreads
from SyncModule import Sync


class Core:
    def __init__(self):
        self.current_lap = 0
        self.all_riders_list = []
        self.current_riders_list = []
        self.race_laps = race_laps
        self.thread_controller = SystemThreads()
        self.sync_module = Sync()

    def start_race(self):
        self.current_lap += 1
        if using_db:
            # sync with db here
            pass
        else:
            while True:
                inp_num = input('Enter rider number: ')
                if 'q' in inp_num or 'Q' in inp_num:
                    break
                try:
                    inp_num = int(inp_num)
                except exception as e:
                    log.info(e)
                self.all_riders_list.append(inp_num)
                print('riders', self.all_riders_list)
        # TODO: need add starting riders list func
        self.thread_controller.start_thread(self.sync_module.start_sync)

    def finish_race(self):
        self.current_lap = 0
        self.current_riders_list = []
        # TODO: need add finish statistic calc func

c = Core()
c.start_race()
