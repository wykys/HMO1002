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

    fr = []
    ph = []
    ku = []
    u1 = []
    u2 = []

    frequency = np.logspace(1, 5, 42)
    for i, f in enumerate(frequency):
        if f > 50e3:
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
        sleep(2 + 12 * period)
        SCPI.stop()

        fr.append(freq.get())
        ph.append(phase.get())
        u1.append(u1_rms.get())
        u2.append(u2_rms.get())

        while any((
            fr[-1] is None,
            ph[-1] is None,
            u1[-1] is None,
            u2[-1] is None,
        )):
            log.war('repeating the measurement')
            SCPI.run()
            SCPI.autoscale()
            SCPI.time_base(period * 2)
            sleep(2 + 12 * period)
            SCPI.stop()
            fr[-1] = freq.get()
            ph[-1] = phase.get()
            u1[-1] = u1_rms.get()
            u2[-1] = u2_rms.get()

        ku.append(20 * np.log10(u2[-1] / u1[-1]))

    plt.subplot(211)
    plt.title('modular frequency response')
    plt.semilogx(fr, ku)
    plt.xlabel('$f$ $[Hz]$')
    plt.ylabel('$K_U$ $[dB]$')
    plt.grid(True, 'major')
    plt.grid(True, 'minor')
    plt.subplot(212)
    plt.title('phase frequency characteristic')
    plt.semilogx(fr, ph)
    plt.xlabel('$f$ $[Hz]$')
    plt.ylabel('$\\varphi$ $[^\circ]$')
    plt.grid(True, 'major')
    plt.grid(True, 'minor')
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

    frequency = np.logspace(1, 5, 400)
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
        sleep(2 + 12 * period)
        SCPI.stop()
        u1.append(u1_rms.get())
        u2.append(u2_rms.get())

        while any((
            u1[-1] is None,
            u2[-1] is None,
            u1[-1] == 9.91e+37,
            u2[-1] == 9.91e+37,
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
