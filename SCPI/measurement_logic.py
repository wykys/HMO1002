import log
import SCPI
import numpy as np
from time import sleep
from matplotlib import pyplot as plt


def module_and_phase_frequency_characteristics():

    freq = SCPI.Measurement(
        measurement=1,
        category=SCPI.MeasType.frequency,
        signal_source=SCPI.Source.channel1,
    )

    phase = SCPI.Measurement(
        measurement=2,
        category=SCPI.MeasType.phase,
        signal_source=SCPI.Source.channel1,
        reference_source=SCPI.Source.channel2,
    )

    u1_rms = SCPI.Measurement(
        measurement=3,
        category=SCPI.MeasType.rms,
        signal_source=SCPI.Source.channel1,
    )

    u2_rms = SCPI.Measurement(
        measurement=4,
        category=SCPI.MeasType.rms,
        signal_source=SCPI.Source.channel2,
    )

    class ModuleAndPhaseCharacteristic:
        def __init__(self, index: int) -> None:
            self.fr = []
            self.ph = []
            self.ku = []
            self.u1 = []
            self.u2 = []
            self.label = f'Channel {index}'

    frequency = np.logspace(1, 5, 100)
    for i, f in enumerate(frequency):
        if f > 25e3:
            frequency = frequency[:i]
            break

    def add_another_channel() -> bool:
        while True:
            log.prompt('Add another channel? yes / no')
            user_input = input().strip().lower()

            if user_input in ['yes', 'y', '']:
                return True

            elif user_input in ['no', 'n']:
                return False

            else:
                log.err(
                    'Incorrect input, possible options are: '
                    'yes, y, no, n or enter'
                )

    data = []
    number_of_channels = 0

    while True:

        number_of_channels += 1
        data.append(ModuleAndPhaseCharacteristic(number_of_channels))

        for i, f in enumerate(frequency, 1):

            period = 1 / f

            log.stdo(f'measurement: {i}/{len(frequency)}')

            SCPI.run()
            SCPI.function_generator(f)
            sleep(2)
            SCPI.autoscale()
            SCPI.time_base(period)
            sleep(3 + 12 * period)
            SCPI.stop()

            data[-1].fr.append(freq.get())
            data[-1].ph.append(phase.get())
            data[-1].u1.append(u1_rms.get())
            data[-1].u2.append(u2_rms.get())

            while any((
                data[-1].fr[-1] is None,
                data[-1].ph[-1] is None,
                data[-1].u1[-1] is None,
                data[-1].u2[-1] is None,
                data[-1].fr[-1] == SCPI.WRONGLY_MEASURED_VALUE,
                data[-1].ph[-1] == SCPI.WRONGLY_MEASURED_VALUE,
                data[-1].u1[-1] == SCPI.WRONGLY_MEASURED_VALUE,
                data[-1].u2[-1] == SCPI.WRONGLY_MEASURED_VALUE,
            )):
                log.war('repeating the measurement')
                SCPI.run()
                SCPI.autoscale()
                sleep(2)
                SCPI.time_base(period * 2)
                sleep(3 + 12 * period)
                SCPI.stop()
                data[-1].fr[-1] = freq.get()
                data[-1].ph[-1] = phase.get()
                data[-1].u1[-1] = u1_rms.get()
                data[-1].u2[-1] = u2_rms.get()

            data[-1].ku.append(
                20 * np.log10(data[-1].u2[-1] / data[-1].u1[-1])
            )

        if not add_another_channel():
            break

    plt.subplot(211)
    plt.title('Module frequency response')
    plt.xlabel('$f$ $[Hz]$')
    plt.ylabel('$K_U$ $[dB]$')
    plt.grid(True, 'major')
    plt.grid(True, 'minor')

    for channel in data:
        plt.semilogx(channel.fr, channel.ku, label=channel.label)

    if number_of_channels > 1:
        plt.legend()

    plt.subplot(212)
    plt.title('Phase frequency characteristic')
    plt.xlabel('$f$ $[Hz]$')
    plt.ylabel('$\\varphi$ $[^\circ]$')
    plt.grid(True, 'major')
    plt.grid(True, 'minor')

    for channel in data:
        plt.semilogx(channel.fr, channel.ph, label=channel.label)

    if number_of_channels > 1:
        plt.legend()

    plt.show()


def module_characteristic_of_both_channels():

    u1_rms = SCPI.Measurement(
        measurement=1,
        category=SCPI.MeasType.rms,
        signal_source=SCPI.Source.channel1,
    )

    u2_rms = SCPI.Measurement(
        measurement=2,
        category=SCPI.MeasType.rms,
        signal_source=SCPI.Source.channel2,
    )

    u1 = []
    u2 = []
    ku1 = []
    ku2 = []

    frequency = np.logspace(1, 5, 10)
    for i, f in enumerate(frequency):

        if f > 20e3:
            frequency = frequency[:i]
            break

    for i, f in enumerate(frequency, 1):

        period = 1 / f

        log.stdo(f'measurement: {i}/{len(frequency)}')

        SCPI.run()
        SCPI.function_generator(f)
        sleep(1)
        SCPI.autoscale()
        SCPI.time_base(period)
        sleep(3 + 12 * period)
        SCPI.stop()
        u1.append(u1_rms.get())
        u2.append(u2_rms.get())

        while any((
            u1[-1] is None,
            u2[-1] is None,
            u1[-1] == SCPI.WRONGLY_MEASURED_VALUE,
            u2[-1] == SCPI.WRONGLY_MEASURED_VALUE,
        )):
            log.war('repeating the measurement')
            SCPI.run()
            SCPI.autoscale()
            SCPI.time_base(period * 2)
            sleep(2 + 12 * period)
            SCPI.stop()
            u1[-1] = u1_rms.get()
            u2[-1] = u2_rms.get()

        ku1.append(20 * np.log10(u1[-1] / 1e-3))
        ku2.append(20 * np.log10(u2[-1] / 1e-3))

    plt.title('Module frequency characteristic')
    plt.semilogx(frequency, ku1, label='Channel 1')
    plt.semilogx(frequency, ku2, label='Channel 2')
    plt.xlabel('$f$ $[Hz]$')
    plt.ylabel('$K_U$ $[dBm]$')
    plt.grid(True, 'major')
    plt.grid(True, 'minor')
    plt.legend()
    plt.show()
