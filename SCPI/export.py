from device import Device
from matplotlib import pyplot as plt


def export():
    Device.send_cmd('FORMat ASCii, 32')
    Device.send_cmd('CHAN1:DATA?')

    response = Device.read_response()

    t = []
    s = []

    response = ''.join(map(lambda x: chr(x), response)).split('\n')[2:-2]
    for line in response:
        tmp = line.split(',')
        t.append(float(tmp[0]))
        s.append(float(tmp[1]))

    plt.plot(t, s)
    plt.grid(True, 'major')
    plt.grid(True, 'minor')
    plt.show()
