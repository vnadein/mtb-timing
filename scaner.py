#!/usr/bin/python3.5
from proximity import *
import math
from time import time
from threading import Thread


class RaceTrackingModule:
        def __init__(self,
                     race_thread_module,
                     racer_id_list={"6966": "1",
                                    "6967": "2",
                                    "6968": "3",
                                    "6969": 4}):
                self.scanner = Scanner(loops=1)
                self.major = "4660"
                self.minor = racer_id_list
                self.startUnit = []
                self.race_thread_module = race_thread_module

        def ratio(self, rssi, tx_rate):
                rssi = int(rssi) * -1
                tx_rate = int(tx_rate) * -1
                ratio = float(rssi) / tx_rate
                return ratio

        def becon_tracking(self, ibecon):
                print("Found racers number :", self.minor[ibecon])
                distance = []
                i = 1
                track = True
                while track:
                        for beacon in self.scanner.scan():
                                beaco = beacon.split(",")
                                if beaco[3] == ibecon and ((beaco[2] == self.major) and (beaco[3] in self.minor)):
                                        if i == 3:
                                                distance.sort()
                                                print('\n[sys] racer ', self.minor[beaco[3]], ' distance', ": ", distance)
                                                if distance[0] < 1:
                                                        race_time = float(time())
                                                        print('\n[sys] racer ', self.minor[beaco[3]], ' finished  -time', ": ", race_time, '\n')
                                                        track = False
                                                distance = []
                                                i = 1
                                        else:
                                                rat = self.ratio(beaco[5],
                                                                 beaco[4])
                                                print('rat', rat)
                                                if rat < 1:
                                                        i += 1
                                                        dist = math.pow(rat, 10)
                                                        distance.append(round(dist, 2))
                                                else:
                                                        i += 1
                                                        dist = 0.89976 * math.pow(rat, 7.7095) + 0.111
                                                        distance.append(round(dist, 2))

        def start(self):
                print("Start searching racers...")
                while True:
                    for beacon in self.scanner.scan():
                        beaco = beacon.split(",")
                        #print('beaco', beaco[3])
                        #print('startunit', self.startUnit)
                        if beaco[3] not in self.startUnit:
                                if (beaco[2] == self.major) and (beaco[3] in self.minor):
                                        self.startUnit.append(beaco[3])
                                        self.race_thread_module.start_thread(self.becon_tracking(beaco[3]), 'ibeacon '+beaco[3])
                                        #print('th finished!!!!')
                                        #thread = Thread(self.becon_tracking(beaco[3])).start()
