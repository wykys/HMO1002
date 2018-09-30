# wykys
# library for basic UART manipulation

import serial
from serial.tools import list_ports

import time
import os
import log


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class UART:
    def __init__(
        self,
        name='HMO1002',
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=None,
        delay=0.01,
        port=None
    ):
        self.name = name
        self.delay = delay
        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.timeout = timeout

        if stopbits == 1:
            self.ser.stopbits = serial.STOPBITS_ONE
        elif stopbits == 2:
            self.ser.stopbits = serial.STOPBITS_TWO

        if port is None:
            self.ser.port = self.find_device()
        else:
            self.ser.port = port
        self.open_connection()

    def __del__(self):
        self.close_connection()

    def cmd_delay(self):
        time.sleep(self.delay)

    def find_device(self):
        for port in list_ports.comports():
            if self.name in port.description:
                return port.device

        log.err(self.name + ' is not connected')
        self.list_ports()
        exit(1)

    def list_ports(self):
        log.stdo('List all connected devices:')
        for port in list_ports.comports():
            print('    ', port.device, '\t', port.description)

    def open_connection(self):
        try:
            self.ser.open()
            log.ok('port {} is open'.format(self.ser.port))
        except serial.SerialException:
            log.err('port {} opening is fail'.format(self.ser.port))
            exit(1)

        self.ser.reset_input_buffer()

    def close_connection(self):
        self.ser.close()
        log.ok('port is close')

    def read_byte(self):
        try:
            tmp = self.ser.read(1)
        except serial.SerialException:
            log.err('the device was disconnected')
            exit()

        if tmp == b'':
            return None
        return int.from_bytes(tmp, byteorder='little', signed=False)

    def send_byte(self, byte):
        try:
            self.ser.write(bytes((byte,)))
        except serial.SerialException:
            log.err('the device was disconnected')
            os.system('killall ser-term')

        time.sleep(0.003)

    def send_cmd(self, cmd):
        if type(cmd) == str:
            for c in cmd:
                self.send_byte(ord(c))
                self.cmd_delay()
            self.send_byte(ord('\n'))
            log.cmd(cmd)


UART = UART()
