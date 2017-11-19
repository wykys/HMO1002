#!/usr/bin/python3
# wykys 2017
# program for control HMO1002 oscilloscope

import argparse
import time
import log
import SI
from SCPI import SCPI

parser = argparse.ArgumentParser('osc')
subparsers = parser.add_subparsers(help='commands')

# screenshot
parser_screenshot = subparsers.add_parser('screenshot', help='save screenshot')
parser_screenshot.add_argument('screenshot', action='store_true', help='save screenshot')
parser_screenshot.add_argument('-f', '--file', dest='file', action='store', default='img', help='image name, withtou siffix')
parser_screenshot.add_argument('-c', '--color', dest='color', action='store', default='color', choices=['color', 'gray', 'invert'], help='image colors')
parser_screenshot.add_argument('-d', '--date', dest='date', action='store_true', default=False, help='add the current date before the name')

# autoscale
parser_autoscale = subparsers.add_parser('autoscale', help='autoscale oscilloscope')
parser_autoscale.add_argument('autoscale', action='store_true', help='run autoscale')

# function generator
parser_fgen = subparsers.add_parser('fgen', help='function generator')
parser_fgen.add_argument('fgen', action='store_true', help='function generator')
parser_fgen.add_argument('-f', '--frequency', dest='freq', action='store', default='1000', help='output frequency')

args = parser.parse_args()

if 'screenshot' in args:
    if args.date:
        name = time.strftime('%Y.%m.%d-%H:%M:%S-', time.localtime()) + args.file
    else:
        name = args.file
    SCPI().screenshot(name=name, color=args.color)

elif 'autoscale' in args:
    SCPI().autoscale()

elif 'fgen' in args:
    SCPI().function_generator(freq=SI.si_to_exp(args.freq))
else:
    log.war('no any argument')
