#!/usr/bin/python3

import os
import time
from socket import socket, AF_INET, SOCK_STREAM

import log
from singleton import singleton


@singleton
class Ethernet:
    def __init__(
        self,
        ip='192.168.1.23',
        port=5025,
    ):
        self.ip = ip
        self.port = port

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.open_connection()

    def __del__(self):
        self.close_connection()

    def open_connection(self):
        try:
            self.socket.connect(self.ip, self.port)
        except:
            log.err(f'socket {self.ip}:{self.port} opening is fail')
            exit(1)

    def close_connection(self):
        self.socket.close()

    def read_byte(self):
        try:
            tmp = self.socket.recv(1).decode('utf-8')
        except:
            log.err('the device was disconnected')
            exit()

        if tmp == b'':
            return None
        return int.from_bytes(tmp, byteorder='little', signed=False)

    def send_byte(self, byte):
        try:
            self.socket.send(bytes((byte,)))
        except:
            log.err('the device was disconnected')

        time.sleep(0.003)

    def send_cmd(self, cmd):
        if type(cmd) == str:
            for c in cmd:
                self.send_byte(ord(c))
                self.cmd_delay()
            self.send_byte(ord('\n'))
            log.cmd(cmd)


Ethernet = Ethernet()
