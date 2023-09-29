from uart import UART
from matplotlib import pyplot as plt


def export():
    UART.send_cmd('FORMat ASCii, 32')
    UART.send_cmd('CHAN1:DATA?')

    result = []
    byte = UART.read_byte()

    while not (byte is None):
        result.append(byte)
        byte = UART.read_byte()

    t = []
    s = []

    result = ''.join(map(lambda x: chr(x), result)).split('\n')[2:-2]
    for line in result:
        tmp = line.split(',')
        t.append(float(tmp[0]))
        s.append(float(tmp[1]))

    plt.plot(t, s)
    plt.grid(True, 'major')
    plt.grid(True, 'minor')
    plt.show()
