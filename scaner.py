from proximity import *
import math
import datetime
from time import time
from threading import Thread

scanner = Scanner(loops=1)
major = "4660"
minor = {"6966": "1", "6967": "2", "6968": "3", "6969": "4"}
startUnit = []

print("Start searching racers...")


def ratio(rssi, tx_rate):
        rssi = int(rssi) * -1
        tx_rate = int(tx_rate) * -1
        ratio = float(rssi) / tx_rate
        return ratio


def becon_tracking(ibecon):
        print("Found racers number :", minor[ibecon])
        distance = []
        i = 1
        while True:
                for beacon in scanner.scan():
                        beaco = beacon.split(",")
                        if beaco[3] == ibecon:
                                if (beaco[2] == major) and (beaco[3] in minor):
                                        if i == 3:
                                                distance.sort()
                                                print(minor[beaco[3]], ": ", distance)
                                                if distance[0] < 1:
                                                        race_time = float(time())
                                                        print(minor[beaco[3]], ": ", race_time)
                                                        return True
                                                distance = []
                                                i = 1
                                        else:
                                                rat = ratio(beaco[5], beaco[4])
                                                if rat < 1:
                                                        i += 1
                                                        dist = math.pow(rat, 10)
                                                        distance.append(round(dist, 2))
                                                else:
                                                        i += 1
                                                        dist = 0.89976 * math.pow(rat, 7.7095) + 0.111
                                                        distance.append(round(dist, 2))

while True:
    for beacon in scanner.scan():
        beaco = beacon.split(",")
        if beaco[3] not in startUnit:
                if (beaco[2] == major) and (beaco[3] in minor):
                        startUnit.append(beaco[3])
                        thread = Thread(becon_tracking, (beaco[3],)).start()
