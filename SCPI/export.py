import log
from device import Device
from matplotlib import pyplot as plt


def export():
    Device.send_cmd('FORMat ASCii, 32')
    Device.send_cmd('CHAN1:DATA?')

    response = b''

    while True:
        tmp = Device.read_response(1024)
        if tmp is None or tmp == b'':
            break
        response += tmp

    if response == b'':
        log.err('problem with data')
        exit(1)

    t = []
    s = []

    response = response.decode('utf-8').split('\n')[2:-2]

    for line in response:
        tmp = line.split(',')
        t.append(float(tmp[0]))
        s.append(float(tmp[1]))

    plt.plot(t, s)
    plt.grid(True, 'major')
    plt.grid(True, 'minor')
    plt.show()
