#!/usr/bin/python3.5
import socket
from config import port
from time import sleep


class Sync:
    def __init__(self):
        self.port = port
        self.sock = socket.socket()

    def get_connection(self, conn_port, conn_addr=''):
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((conn_addr, conn_port))
        self.sock.settimeout(1.2)
        self.sock.listen(2)
        while True:
            conn = None
            addr = None
            while True:
                try:
                    conn, addr = self.sock.accept()
                    print('Connection established: %s %s' % (
                    str(conn), str(addr)))
                    return conn, addr
                except Exception as e:
                    print(e)
                    sleep(0.246)

    def resieve(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                sleep(0.246)
                continue
            else:
                print('\nrecieved data: \n', data.decode('cp1251'))
                return data

    def start_sync(self):
        sync = Sync()
        conn, addr = sync.get_connection(sync.port)
        sync.resieve(conn)
