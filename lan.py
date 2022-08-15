#!/usr/bin/python3

import socket

OSC_IP = '192.168.1.8'
OSC_PORT = 5025

if __name__ == '__main__':
    print('Hello')

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((OSC_IP, OSC_PORT))

    s.send(bytes('*IDN?\n', 'utf-8'))
    res = s.recv(1000).decode('utf-8')

    s.close()

    print(res)
