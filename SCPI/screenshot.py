import log
from device import Device
import SCPI


def screenshot(name='img', color='color'):
    SCPI.stop()
    Device.send_cmd('HCOPy:FORMat PNG')

    if color == 'color':
        Device.send_cmd('HCOPy:COLOR:SCHeme COLor')
    elif color == 'gray':
        Device.send_cmd('HCOPy:COLOR:SCHeme GRAYscale')
    else:
        Device.send_cmd('HCOPy:COLOR:SCHeme INVerted')

    Device.send_cmd('HCOPy:DATA?')

    if Device.read_response(1).decode('utf-8') != '#':
        log.err('# not found')
        exit(1)

    size_head = int(Device.read_response(1))
    size_image = int(Device.read_response(size_head))

    img = Device.read_response(size_image)
    while len(img) < size_image:
        tmp = Device.read_response(size_image - len(img))
        if tmp is None:
            break
        img += tmp

    if len(img) != size_image:
        log.err('bad image data')
        exit(1)

    fw = open(name + '.png', 'wb')
    fw.write(img)
    fw.close()

    SCPI.run()
