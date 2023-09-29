# wykys 2018

from rich import print
from sys import stdout, stderr


def err(s=''):
    print(f'[bold red]ERROR: {s}[/]', file=stderr)


def war(s=''):
    print(f'[bold yellow]WARNING: {s}[/]', file=stderr)


def ok(s=''):
    print(f'[bold green]OK: {s}[/]', file=stdout)


def stdo(s=''):
    print(f'[bold white]{s}[/]', file=stdout)


def cmd(s=''):
    print(f'[bold cyan]CMD: {s}[/]', file=stdout)


def rx(s='', prompt=True):
    print(f'\r[bold violet]RX: {s}[/]', file=stdout, end='')
    if prompt:
        print(f'\n[bold blue]>>> ', file=stdout, end='')


def tx(s=''):
    print(f'[bold green]TX: {s}[/]', file=stdout)
