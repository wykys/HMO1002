from device import Device


def function_generator(freq):
    Device.send_cmd(f'GENerator:FREQuency {float(freq):e}')
