from proximity import *
import math
import datetime
from time import time
import thread

scanner = Scanner(loops=1)
units = {"6966": "1", "6967": "2", "6968" : "3", "6969" : "4"}
startUnit = []

def beconTracking(ibecon):
        print "Thread start for :", units[ibecon]
        distance = []
        i = 1
        while True:
                for beacon in scanner.scan():
                        beaco = beacon.split(",")
                        if(beaco[3] == ibecon):
                                if ((beaco[2] == "4660") and (beaco[3] in units)):
                                        rssi = int(beaco[5])
                                        rssi *= -1
                                        tx_rate = int(beaco[4])
                                        tx_rate *= -1
                                        rat = float(rssi) / tx_rate
                                        if (i == 3):
                                                distance.sort()
                                                print distance
                                                if(distance[0] < 1):
                                                        raceTime = float(time())
                                                        print units[beaco[3]], ": ", raceTime
                                                        return True
                                                distance = []
                                                i = 1
                                        else:
                                                if (rat < 1):
                                                        i += 1
                                                        dist = math.pow(rat, 10)
                                                        distance.append(round(dist,2))
                                                else:
                                                        i += 1
                                                        dist = 0.89976 * math.pow(rat, 7.7095) + 0.111
                                                        distance.append(round(dist,2))

while True:
    for beacon in scanner.scan():
        beaco = beacon.split(",")
        if(beaco[3] not in startUnit):
                if ((beaco[2] == "4660") and (beaco[3] in units)):
                        startUnit.append(beaco[3])
                        thread.start_new_thread(beconTracking,(beaco[3],))