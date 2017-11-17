#!/usr/bin/python3.5
from proximity import *
import math
from threading import Thread
from config import *
from time import time


class RaceTrackingModule:
        def __init__(self, race_thread_module, racer_id_list, finish_cb, start_cb):
                print(paint("Scaner init...", GREEN))
                self.scanner = Scanner(loops=1)
                self.major = "4660"
                self.minor = racer_id_list
                print(paint('Riders list : ', CYAN), self.minor)
                self.startUnit = []
                self.race_thread_module = race_thread_module
                self.finish_cb = finish_cb
                self.start_cb = start_cb
                self.stop = False
                self.stop_track = False
                self.beacon_temp = None

        def ratio(self, rssi, tx_rate):
                rssi = int(rssi) * -1
                tx_rate = int(tx_rate) * -1
                ratio = float(rssi) / tx_rate
                return ratio

        def becon_tracking(self):
                ibecon = self.beacon_temp
                print(paint("[sys][scaner] Found racer id : " + str(ibecon), GREEN))
                distance = []
                i = 1
                track = True
                while track and not self.stop_track:
                        st = time()
                        for beacon in self.scanner.scan():
                                beaco = beacon.split(",")
                                if beaco[3] == ibecon and ((beaco[2] == self.major) and (beaco[3] in self.minor)):
                                        if i == 4:
                                                distance.sort()
                                                #print('\n', paint('[sys][scaner] racer ', GREEN), beaco[3], paint(' distance : ', MAGENTA), distance)
                                                mid = 0
                                                count = 0
                                                for i in distance:
                                                        mid += i
                                                        count += 1
                                                #print('average', mid/count)

                                                #if distance[0] < 1:
                                                if (mid/count) < 1:
                                                        race_time = float(time())
                                                        print('\n[sys] racer ', beaco[3], ' finished  -time', ": ", race_time, '\n')
                                                        track = False
                                                        self.finish_cb(beaco[3], race_time)
                                                distance = []
                                                i = 1
                                        else:
                                                rat = self.ratio(beaco[5],
                                                                 beaco[4])
                                                #print('ratio : ', rat)
                                                if rat < 1:
                                                        i += 1
                                                        dist = math.pow(rat, 10)
                                                        distance.append(round(dist, 2))
                                                else:
                                                        i += 1
                                                        dist = 0.89976 * math.pow(rat, 7.7095) + 0.111
                                                        distance.append(round(dist, 2))
                                        ft = time()
                                        #print('performance : ', ft-st)

        def start(self):
                self.stop = False
                self.stop_track = False
                print("Start searching racers...")
                while True and not self.stop:
                    for beacon in self.scanner.scan():
                        beaco = beacon.split(",")
                        #print('11111111111', beaco[3])
                        #print('11111111111', beaco[3] in self.minor)
                        if beaco[3] not in self.startUnit and (beaco[2] == self.major) and (beaco[3] in self.minor):
                                self.start_cb(beaco[3], float(time()))
                                self.startUnit.append(beaco[3])
                                self.beacon_temp = beaco[3]
                                self.race_thread_module.start_thread(self.becon_tracking, name='ibeacon '+beaco[3])
