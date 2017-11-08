#!/usr/bin/python3.5
import blescan
import bluetooth._bluetooth as bluez


class Scanner:
    def __init__(self, device_id=0, loops=1):
        self.deviceId = device_id
        self.loops = loops
        try:
            self.sock = bluez.hci_open_dev(self.deviceId)
            blescan.hci_le_set_scan_parameters(self.sock)
            blescan.hci_enable_le_scan(self.sock)
        except Exception as e:
            print(e)

    def scan(self):
        return blescan.parse_events(self.sock, self.loops)

    def test(self):
        while True:
            for beacon in self.scan():
                print(beacon)
