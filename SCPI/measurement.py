import log
from device import Device

MEASUREMENT_MIN = 1
MEASUREMENT_MAX = 6


class Measure:
    pass


class Source:
    channel1 = 'CH1'
    channel2 = 'CH2'


class State:
    on = 'ON'
    off = 'OFF'


class MeasType:
    frequency = 'FREQuency'
    period = 'PERiod'
    peak = 'PEAK'
    upeakvalue = 'UPEakvalue'
    lpeakvalue = 'LPEakvalue'
    ppcount = 'PPCount'
    npcount = 'NPCount'
    recount = 'RECount'
    fecount = 'FECount'
    high = 'HIGH'
    low = 'LOW'
    amplitude = 'AMPLitude'
    crest = 'CRESt'
    mean = 'MEAN'
    rms = 'RMS'
    rtime = 'RTIMe'
    ftime = 'FTIMe'
    pdcycle = 'PDCycle'
    ndcycle = 'NDCycle'
    ppwidth = 'PPWidth'
    npwidth = 'NPWidth'
    cycmean = 'CYCMean'
    cycrms = 'CYCRms'
    stddev = 'STDDev'
    tfrequency = 'TFRequency'
    tperiode = 'TPERiode'
    delay = 'Delay'
    phase = 'Phase'
    bwidth = 'BWIDth'
    povershoot = 'POVershoot'
    novershoot = 'NOVershoot'


def quick_measurement_on(measurement: int) -> None:
    Device.send_cmd(f'MEASurement{measurement:d}:AON')


def quick_measurement_off(measurement: int) -> None:
    Device.send_cmd(f'MEASurement{measurement:d}:AOFF')


def measurement_state(measurement: int, state: str) -> None:
    Device.send_cmd(f'MEASurement{measurement:d}:ENABLE {state}')


def measurement_set_source(
    measurement: int,
    signal_source: str,
    reference_source: str = None,
) -> None:
    if reference_source is None:
        Device.send_cmd(f'MEASurement{measurement:d}:SOURce {signal_source}')
    else:
        Device.send_cmd(
            f'MEASurement{measurement:d}:'
            f'SOURce {signal_source}, {reference_source}'
        )


def measurement_set_category(measurement: int, category: str) -> None:
    Device.send_cmd(f'MEASurement{measurement:d}:MAIN {category}')


def measurement_result(measurement: int):
    Device.send_cmd(f'MEASurement{measurement:d}:RESult?')

    response = Device.read_response()

    if response is None or len(response) == 0:
        response = None
    else:
        response = float(
            ''.join(map(lambda c: chr(c), response))
        )

    log.measurement(response)
    return response


class Measurement:
    def __init__(
        self,
        measurement=None,
        category=None,
        signal_source=None,
        reference_source=None
    ):
        self.measurement = measurement
        self.category = category
        self.signal_source = signal_source
        self.reference_source = reference_source

        self.on()
        measurement_set_source(
            self.measurement, self.signal_source, self.reference_source)
        measurement_set_category(self.measurement, self.category)

    def on(self):
        measurement_state(self.measurement, 'ON')

    def off(self):
        measurement_state(self.measurement, 'OFF')

    def get(self):
        return measurement_result(self.measurement)
