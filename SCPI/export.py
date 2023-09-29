from device import Device
from matplotlib import pyplot as plt


def export():
    Device.send_cmd('FORMat ASCii, 32')
    Device.send_cmd('CHAN1:DATA?')

    result = []
    byte = Device.read_byte()

    while not (byte is None):
        result.append(byte)
        byte = Device.read_byte()

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
