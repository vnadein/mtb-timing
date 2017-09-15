from config import *
from sthreads import SystemThreads
from SyncModule import Sync


class Core:
    def __init__(self):
        self.current_lap = 0
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
            # generate or input riders id`s
            pass
        # TODO: need add starting riders list func
        self.thread_controller.start_thread(self.sync_module.start_sync)

    def finish_race(self):
        self.current_lap = 0
        self.current_riders_list = []
        # TODO: need add finish statistic calc func

c = Core()
c.start_race()
