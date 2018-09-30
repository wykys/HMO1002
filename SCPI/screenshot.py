import log
from uart import UART


def screenshot(name='img', color='color'):
    UART.send_cmd('STOP')
    UART.send_cmd('HCOPy:FORMat PNG')

    if color == 'color':
        UART.send_cmd('HCOPy:COLOR:SCHeme COLor')
    elif color == 'gray':
        UART.send_cmd('HCOPy:COLOR:SCHeme GRAYscale')
    else:
        UART.send_cmd('HCOPy:COLOR:SCHeme INVerted')

    UART.send_cmd('HCOPy:DATA?')

    if chr(UART.read_byte()) != '#':
        log.err('# not found')
        exit(1)

    size_len = UART.read_byte()
    if size_len is None:
        log.err('no data')
        exit(1)
    size_len = int(size_len - ord('0'))

    bytes_len = []
    for i in range(size_len):
        tmp = UART.read_byte()
        if tmp is None:
            log.err('no data')
            exit(1)
        bytes_len.append(tmp)
    bytes_len = int(bytes(bytes_len), 10)

    img = []
    for i in range(bytes_len):
        tmp = UART.read_byte()
        if tmp is None:
            log.err('no data')
            exit(1)
        img.append(tmp)
    img = bytes(img)

    fw = open(name + '.png', 'wb')
    fw.write(img)
    fw.close()

    UART.send_cmd('RUN')
