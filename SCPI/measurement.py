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


def _check_measurement(measurement):
    if measurement >= MEASUREMENT_MIN and measurement <= MEASUREMENT_MAX:
        return True
    else:
        return False


# quick measurement
def quick_measurement_on(measurement):
    Device.send_cmd('MEASurement{:d}:AON'.format(measurement))


# quick measurement
def quick_measurement_off(measurement):
    Device.send_cmd('MEASurement{:d}:AOFF'.format(measurement))


def measurement_state(measurement, state):
    Device.send_cmd('MEASurement{:d}:ENABLE {}'.format(
        measurement, state
    ))


def measurement_set_source(measurement, signal_source, reference_source=None):
    if reference_source is None:
        Device.send_cmd('MEASurement{:d}:SOURce {}'.format(
            measurement, signal_source
        ))
    else:
        Device.send_cmd('MEASurement{:d}:SOURce {}, {}'.format(
            measurement, signal_source, reference_source
        ))


def measurement_set_category(measurement, category):
    Device.send_cmd('MEASurement{:d}:MAIN {}'.format(
        measurement, category
    ))


def measurement_result(measurement):
    Device.send_cmd('MEASurement{:d}:RESult?'.format(
        measurement
    ))

    result = []
    byte = Device.read_byte()

    while not (byte is None):
        result.append(byte)
        byte = Device.read_byte()

    return None if len(result) == 0 else float(''.join(map(lambda c: chr(c), result)))


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
        measurement_set_source(self.measurement, self.signal_source, self.reference_source)
        measurement_set_category(self.measurement, self.category)

    def on(self):
        measurement_state(self.measurement, 'ON')

    def off(self):
        measurement_state(self.measurement, 'OFF')

    def get(self):
        return measurement_result(self.measurement)
