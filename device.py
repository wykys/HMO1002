import log
from singleton import singleton


class InterfaceNone:

    def error_message(self):
        log.err('the communication interface is not initialized')

    def send_cmd(self, cmd) -> None:
        self.error_message()

    def read_byte(self):
        self.error_message()


@singleton
class Device:
    def __init__(self) -> None:
        self.interface = InterfaceNone()

    def slect_uart(self) -> None:
        from uart import Uart
        self.interface = Uart()

    def select_ethernet(self) -> None:
        from ethernet import Ethernet
        self.interface = Ethernet()

    def send_cmd(self, cmd: str) -> None:
        self.interface.send_cmd(cmd)

    def read_response(self):
        return self.interface.read_response()


Device = Device()
