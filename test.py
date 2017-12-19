from proximity import *
import math
scanner = Scanner(loops=3)
i = 0
mid_range = 0


def ratio(rssi, tx_rate):
    rssi = int(rssi) * -1
    tx_rate = int(tx_rate) * -1
    ratio = float(rssi) * 1.0 / tx_rate
    return ratio

while True:
    for beacon in scanner.scan():
        beaco = beacon.split(',')
        rat = 0
        if i == 3:
            print((mid_range/i))
            if int(beaco[4])>0:
                rat = ratio(mid_range/i, int(beaco[4]))
            i = 0
            mid_range = 0
        else:
            mid_range += int(beaco[5])
            i += 1

        if rat < 1:
            dist = math.pow(rat, 10)
            # distance.append(round(dist, 2))
            print('dist < 1', round(dist, 2))
        else:
            dist = 0.89976 * math.pow(rat, 7.7095) + 0.111
            # distance.append(round(dist, 2))
            print('dist > 1', round(dist, 2))
