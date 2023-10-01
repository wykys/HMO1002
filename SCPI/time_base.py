from device import Device


def time_base(time_scale: float):
    Device.send_cmd(f'TIMebase:SCALe {float(time_scale):e}')
