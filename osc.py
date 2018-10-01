#!/usr/bin/python3
# wykys 2017
# program for control HMO1002 oscilloscope

import argparse
import time
import log
import SI
import SCPI

parser = argparse.ArgumentParser('osc')
subparsers = parser.add_subparsers(help='commands')

# screenshot
parser_screenshot = subparsers.add_parser(
    'screenshot',
    help='save screenshot',
)
parser_screenshot.add_argument(
    'screenshot',
    action='store_true',
    help='save screenshot',
)
parser_screenshot.add_argument(
    '-f',
    '--file',
    dest='file',
    action='store',
    default='img',
    help='image name, withtou siffix',
)
parser_screenshot.add_argument(
    '-c',
    '--color',
    dest='color',
    action='store',
    default='color',
    choices=['color', 'gray', 'invert'],
    help='image colors',
)
parser_screenshot.add_argument(
    '-d',
    '--date',
    dest='date',
    action='store_true',
    default=False, help='add the current date before the name'
)

# autoscale
parser_autoscale = subparsers.add_parser(
    'autoscale',
    help='autoscale oscilloscope'
)
parser_autoscale.add_argument(
    'autoscale',
    action='store_true',
    help='run autoscale'
)

# function generator
parser_fgen = subparsers.add_parser(
    'fgen',
    help='function generator'
)
parser_fgen.add_argument(
    'fgen',
    action='store_true',
    help='function generator'
)
parser_fgen.add_argument(
    '-f',
    '--frequency',
    dest='freq',
    action='store',
    default='1000',
    help='output frequency'
)

# auto measurement
# autoscale
parser_measurement = subparsers.add_parser(
    'measurement',
    help='autoscale oscilloscope'
)
parser_measurement.add_argument(
    'measurement',
    action='store_true',
    help='run xxxxxxxxx'
)

args = parser.parse_args()

if 'screenshot' in args:
    if args.date:
        name = time.strftime('%Y.%m.%d-%H:%M:%S-', time.localtime()) + args.file
    else:
        name = args.file
    SCPI.screenshot(name=name, color=args.color)

elif 'autoscale' in args:
    SCPI.autoscale()

elif 'fgen' in args:
    SCPI.function_generator(freq=SI.si_to_exp(args.freq))

elif 'measurement' in args:
    import numpy as np
    from matplotlib import pyplot as plt
    from time import sleep

    freq = SCPI.Measurement(1, SCPI.MeasType.frequency, SCPI.Source.channel1)
    phase = SCPI.Measurement(2, SCPI.MeasType.phase, SCPI.Source.channel1, SCPI.Source.channel2)
    u1_rms = SCPI.Measurement(3, SCPI.MeasType.rms, SCPI.Source.channel1)
    u2_rms = SCPI.Measurement(4, SCPI.MeasType.rms, SCPI.Source.channel2)

    fr = []
    ph = []
    ku = []
    u1 = []
    u2 = []

    frequency = np.logspace(1, 5, 20)[:-2]
    for i, f in enumerate(frequency, 1):
        log.stdo('measurement: {}/{}'.format(i, len(frequency)))

        SCPI.function_generator(f)
        SCPI.autoscale()
        sleep(5)
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
            SCPI.autoscale()
            sleep(5)
            fr[-1] = freq.get(),
            ph[-1] = phase.get(),
            u1[-1] = u1_rms.get(),
            u2[-1] = u2_rms.get(),

        try:
            ku.append(20*np.log10(u2[-1]/u1[-1]))
        except TypeError:
            log.war('problem on freq {:e} Hz'.format(f))

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

else:
    log.war('no any argument')
