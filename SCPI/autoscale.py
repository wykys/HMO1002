from uart import UART


def autoscale():
    UART.send_cmd('AUToscale')
