from device import Device


def run():
    Device.send_cmd('RUN')


def stop():
    Device.send_cmd('STOP')
