#!/usr/bin/env python3
# wykys 2017
# program for control HMO1002 oscilloscope

import argparse
import time
import log
import SI
import SCPI

from device import Device

parser = argparse.ArgumentParser('osc')

parser.add_argument(
    '-i',
    '--interface',
    dest='interface',
    action='store',
    default='uart',
    choices=['uart', 'ethernet'],
    help='communication interface with the device',
)

parser.add_argument(
    '-p',
    '--ip',
    dest='ip',
    action='store',
    default='192.168.1.12',
    help='ip address of the oscilloscope',
)

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

# time base
parser_time_base = subparsers.add_parser(
    'time_base',
    help='sets the horizontal scale for all channel and math waveforms'
)
parser_time_base.add_argument(
    'time_base',
    action='store_true',
    help='sets the horizontal scale for all channel and math waveforms'
)
parser_time_base.add_argument(
    '-t',
    '--time',
    dest='time_scale',
    action='store',
    default=1e-3,
    help='time scale'
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
parser_measurement = subparsers.add_parser(
    'measurement',
    help='starts the automatic measurement'
)
parser_measurement.add_argument(
    'measurement',
    action='store_true',
    help='starts the automatic measurement'
)
parser_measurement.add_argument(
    '-t',
    '--type',
    dest='type',
    action='store',
    default='module_and_phase_frequency_characteristics',
    choices=[
        'module_and_phase_frequency_characteristics',
        'module_characteristic_of_both_channels',
    ],
    help='type of measurement',
)

# export
parser_measurement = subparsers.add_parser(
    'export',
    help='export data'
)
parser_measurement.add_argument(
    'export',
    action='store_true',
    help='export data'
)

args = parser.parse_args()

if args.interface == 'uart':
    Device.slect_uart()
else:
    Device.select_ethernet(args.ip)

if 'screenshot' in args:
    if args.date:
        name = time.strftime(
            '%Y.%m.%d-%H:%M:%S-',
            time.localtime()
        ) + args.file
    else:
        name = args.file
    SCPI.screenshot(name=name, color=args.color)

elif 'autoscale' in args:
    SCPI.autoscale()

elif 'time_base' in args:
    SCPI.time_base(time_scale=SI.si_to_exp(args.time_scale))

elif 'fgen' in args:
    SCPI.function_generator(freq=SI.si_to_exp(args.freq))

elif 'measurement' in args:
    if args.type == 'module_and_phase_frequency_characteristics':
        SCPI.module_and_phase_frequency_characteristics()
    elif args.type == 'module_characteristic_of_both_channels':
        SCPI.module_characteristic_of_both_channels()

elif 'export' in args:
    SCPI.export()

else:
    log.war('no any argument')
