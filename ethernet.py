#!/usr/bin/python3

import log
from singleton import singleton
from socket import socket, AF_INET, SOCK_STREAM


@singleton
class Ethernet:
    def __init__(
        self,
        ip='192.168.1.12',
        port=5025,
    ) -> None:
        self.ip = ip
        self.port = port

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(1.5)
        self.open_connection()

    def __del__(self) -> None:
        self.close_connection()

    def open_connection(self) -> None:
        try:
            self.socket.connect((self.ip, self.port))
            log.ok(f'socket {self.ip}:{self.port} is open')
        except:
            log.err(f'socket {self.ip}:{self.port} opening is fail')
            exit(1)

    def close_connection(self) -> None:
        self.socket.close()

    def read_response(self, size: int) -> bytes | None:
        try:
            response = self.socket.recv(size)

        except TimeoutError:
            response = b''

        except:
            log.err('the device was disconnected')
            exit(1)

        if response == b'':
            return None

        return response

    def send_cmd(self, cmd: str) -> None:
        try:
            self.socket.send(bytes(f'{cmd}\n', 'utf-8'))
            log.cmd(cmd)
        except:
            log.err('the device was disconnected')
