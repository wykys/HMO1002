import sys
from colors import colors

def err(s = ''):
    print( colors.fg.red + colors.bold + 'Error: ' + s + colors.reset, file=sys.stderr)

def war(s = ''):
    print( colors.fg.yellow + colors.bold + 'Warning: ' + s + colors.reset, file=sys.stderr)

def ok(s = ''):
    print( colors.fg.green + colors.bold + 'OK: ' + s + colors.reset, file=sys.stdout)

def stdo(s = ''):
    print( colors.fg.white + colors.bold + s + colors.reset, file=sys.stdout)
