# wykys 2018

from rich import print
from sys import stderr


def err(s: str = '') -> None:
    print(f'[bold red]ERROR: {s}[/]', file=stderr)


def war(s: str = '') -> None:
    print(f'[bold yellow]WARNING: {s}[/]', file=stderr)


def ok(s: str = '') -> None:
    print(f'[bold green]OK: {s}[/]')


def stdo(s: str = '') -> None:
    print(f'[bold white]{s}[/]')


def cmd(s: str = '') -> None:
    print(f'[bold cyan]CMD: {s}[/]')


def rx(s: str = '', prompt: bool = True) -> None:
    print(f'\r[bold violet]RX: {s}[/]', end='')
    if prompt:
        print('\n[bold blue]>>> ', end='')


def tx(s: str = '') -> None:
    print(f'[bold green]TX: {s}[/]')


def measurement(s: str = '') -> None:
    print(f'[bold dark_orange]MEAS: {s}[/]')


def prompt(s: str = '') -> None:
    print(f'[bold green_yellow]{s}[/] >>> ', end='')
