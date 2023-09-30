# wykys
# library for basic UART manipulation

import serial
from serial.tools import list_ports

import log
from singleton import singleton


@singleton
class Uart:
    def __init__(
        self,
        name='HMO1002',
        baudrate=115200,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1.5,
        port=None
    ) -> None:
        self.name = name
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

    def __del__(self) -> None:
        self.close_connection()

    def find_device(self) -> None:
        for port in list_ports.comports():
            if self.name in port.description:
                return port.device

        log.err(self.name + ' is not connected')
        self.list_ports()
        exit(1)

    def list_ports(self) -> None:
        log.stdo('List all connected devices:')
        for port in list_ports.comports():
            log.stdo(f'    {port.device}\t{port.description}')

    def open_connection(self) -> None:
        try:
            self.ser.open()
            log.ok(f'port {self.ser.port} is open')
        except serial.SerialException:
            log.err(f'port {self.ser.port} opening is fail')
            exit(1)

        self.ser.reset_input_buffer()

    def close_connection(self) -> None:
        self.ser.close()

    def read_byte(self) -> bytes:
        try:
            response = self.ser.read(1)
        except serial.SerialException:
            log.err('the device was disconnected')
            exit()
        return response

    def read_response(self, size: int) -> bytes | None:
        response = b''
        for i in range(size):
            tmp = self.read_byte()
            response += tmp

            if tmp == b'':
                break

        if response == b'':
            return None

        return response

    def send_byte(self, byte) -> None:
        try:
            self.ser.write(bytes((byte,)))
        except serial.SerialException:
            log.err('the device was disconnected')

    def send_cmd(self, cmd: str) -> None:
        if type(cmd) == str:
            for c in cmd:
                self.send_byte(ord(c))
            self.send_byte(ord('\n'))
            log.cmd(cmd)
