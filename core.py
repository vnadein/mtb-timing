#!/usr/bin/python3.5
from config import *
from sthreads import SystemThreads
from SyncModule import Sync
from scaner import RaceTrackingModule
from DataTable import DataTable


class Core:
    def __init__(self):
        self.current_lap = 0  # not used
        self.all_riders_list = []
        self.current_riders_list = []
        self.race_laps = race_laps  # not used
        self.thread_controller = SystemThreads()
        self.sync_module = Sync()
        self.db = DataTable()
        self.t_module = None

    def start_race(self):
        self.current_lap += 1
        if test_mode:
            self.test_menu()
        else:
            self.t_module = RaceTrackingModule(self.thread_controller,
                                               racer_id_list=self.db.get_internal_riderslist(),
                                               finish_cb=self.write_racer_finish_time,
                                               start_cb=self.write_racer_start_time)
        log.info("[core] Rider list ready!")
        self.thread_controller.start_thread(self.sync_module.start_sync)
        log.info("[core] Sync module started!")
        self.thread_controller.start_thread(self.t_module.start)
        log.info("[core] Racer track module started!")

    def test_menu(self):
        # this menu need only for testing
        print(paint('TEST MODE!', RED))
        while True:
            print(paint('For help use - "help"', BLUE))
            inp = input(paint('Enter command : ', GREEN))
            if 'help' in inp:
                print(paint('prepare DB to test : ', RED_INV), 'db_set_test')
                print(paint('start test race! : ', RED_INV), 'race_start')
                print(paint('restart test race! : ', RED_INV), 'race_restart')
                print(paint('for exit : ', RED_INV), 'exit')
                print(paint('for skip menu : ', RED_INV), 'q')
            elif 'exit' in inp:
                print(paint('EXIT', RED))
                exit()
            elif 'q' in inp:
                print(paint('CONTINUE!', GREEN))
                break
            elif 'db_set_test' in inp:
                self.db.clear_all_riders()
                self.db.clear_chip_list()
                self.db.add_chip(1000)
                self.db.add_chip(6967)
                self.db.add_chip(4000)
                self.db.add_chip(5000)
                self.db.add_new_rider('test_1', 'test_1', 1)
                self.db.add_new_rider('test_2', 'test_2', 2)
                self.db.add_new_rider('test_3', 'test_3', 3)
                self.db.add_new_rider('test_4', 'test_4', 4)
            elif 'race_start' in inp:
                self.t_module = RaceTrackingModule(self.thread_controller,
                                                   racer_id_list=self.db.get_internal_riderslist(),
                                                   finish_cb=self.write_racer_finish_time,
                                                   start_cb=self.write_racer_start_time)
                log.info("[core] Rider list ready!")
                self.thread_controller.start_thread(self.sync_module.start_sync)
                log.info("[core] Sync module started!")
                self.thread_controller.start_thread(self.t_module.start, name='Tracking')
                log.info("[core] Racer track module started!")
            elif 'race_restart' in inp:
                self.t_module.stop_track = True
                self.t_module.stop = True
                print('Race stopped!')
            else:
                print('MENU ERROR')
                pass

    def write_racer_finish_time(self, rider_id, finish_ts):
        self.db.set_finish_ts(rider_id=int(rider_id), finish_ts=finish_ts)

    def write_racer_start_time(self, rider_id, start_ts):
        self.db.set_start_time(rider_id=int(rider_id), start_ts=start_ts)

    def finish_race(self):  # not used
        self.current_lap = 0
        self.current_riders_list = []
        # TODO: need add finish statistic calc func

    def registration(self):  # not used
        # self.db
        pass

c = Core()
c.start_race()
