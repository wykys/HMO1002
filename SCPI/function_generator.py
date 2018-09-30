from uart import UART


def function_generator(freq):
    UART.send_cmd('GENerator:FREQuency {:e}'.format(float(freq)))
