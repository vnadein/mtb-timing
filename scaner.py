from proximity import *
import math

scanner = Scanner(loops=1)
while True:
    for beacon in scanner.scan():
        beaco = beacon.split(",")
        if (beaco[3] == "6645"):
                rssi = int(beaco[5])
                rssi *= -1
                tx_rate = int(beaco[4])
                tx_rate *= -1
                rat = float(rssi) / tx_rate
                if (rat <1):
                        dist = math.pow(rat, 10)
                        print "Distance is :", round(dist, 2), " Number :", beaco[2]
                else:
                        dist = 0.89976 * math.pow(rat, 7.7095) + 0.111
                        print "Distance is :", round(dist, 2), " Number :", beaco[2]